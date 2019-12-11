# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from celery.utils.log import get_task_logger
from servalx import (
    androzoo,
    artifacts,
    couch,
    elastic,
    extractions,
    features,
    virustotal,
)

from . import config
from .celery import app

LOGGER = get_task_logger(__name__)

COUCH = couch.Connection(config.couch_endpoint)

ELASTIC = elastic.Connection(config.elastic_urls, timeout=240)

ANDROZOO = androzoo.AndrozooAPI(config.androzoo_apikey, config.androzoo_apiurl)

VIRUSTOTAL = virustotal.VirusTotalAPI(config.virustotal_apikey)


@app.task(retry=True, default_retry_delay=3600)
def migrate(sha256):
    """Migrate database documents from couch to elastic."""
    infos = couch.get_or_none(COUCH, COUCH.DB_APKINFOS, sha256)
    metas = couch.get_or_none(COUCH, COUCH.DB_APKMETAS, sha256)
    labels = couch.get_or_none(COUCH, COUCH.DB_APKLABELS, sha256)

    metas = artifacts.from_metas(metas) if metas is not None else {}
    infos = artifacts.from_apkinfos(infos) if infos is not None else {}
    labels = artifacts.from_labels(labels) if labels is not None else {}

    doc = {str(k): list(v) for k, v in metas.items() + infos.items() + labels.items()}

    return elastic.index(ELASTIC, ELASTIC.IDX_APKINDEX, sha256, doc)


@app.task
def apkfile(sha256):
    """"Extract information from an APK file."""
    apkfile = androzoo.download(ANDROZOO, sha256)

    apk = Apk.APK(apkfile.read())
    doc = extractions.apk(apk)

    yield COUCH.DB_APKINFOS, sha256, doc


@app.task
def apkfeat(sha256):
    """Compute features from an APK infos."""
    infos = couch.get(COUCH, COUCH.DB_APKINFOS, sha256)
    doc = features.from_apkinfos(infos)

    yield COUCH.DB_APKFEATS, sha256, doc


@app.task(
    rate_limit='1000/m',
    default_retry_default=24 * 3600,
    autoretry_for=(virustotal.APILimitExceeded, virustotal.ItemIsCurrentlyQueued))
def vtreport(sha256):
    """Retrieve a report from virustotal from an APK sha256.."""
    doc = virustotal.file_report(VIRUSTOTAL, sha256)

    yield COUCH.DB_VIRUSTOTAL, sha256, doc


@app.task(rate_limit='1000/m')
def vtscan(sha256):
    """Send a scan request to virustotal from an APK sha256.."""
    apkfile = androzoo.download(ANDROZOO, sha256)

    return virustotal.file_scan(VIRUSTOTAL, apkfile.getvalue())


@app.task(rate_limit='1000/m')
def vtrescan(sha256):
    """Send a rescan request to virustotal from an APK sha256.."""
    return virustotal.file_rescan(VIRUSTOTAL, sha256)
