#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from celery import Celery

from . import config

app = Celery("apkworkers", include=["apkworkers.actions"])
app.config_from_object(config)

if __name__ == "__main__":
    app.start()
