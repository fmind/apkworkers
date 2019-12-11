# -*- coding: utf-8 -*-

from setuptools import setup

PROJECT = "apkworkers"
PACKAGE = "apkworkers"
VERSION = "1.7.0"
LICENSE = "LGPL-3.0"
USERNAME = "fmind"
AUTHOR = u"Médéric Hurier (fmind)"
COPYRIGHT = u"2019, Médéric Hurier"
EMAIL = "fmind@fmind.me"
URL = "https://github.com/fmind/apkworkers"

DESC = "A Celery application to distribute Android malware analysis."

DOC = DESC

PLATFORMS = "any"

KEYWORDS = [PACKAGE]

PACKAGES = [PACKAGE]

SCRIPTS = ["bin/workdo", "bin/workvt"]

CLASSIFIERS = [
    "Operating System :: POSIX",
    "Natural Language :: English",
    "Intended Audience :: Developers",
    "Development Status :: 2 - Pre-Alpha",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: Implementation :: CPython",
]

REQUIRES = {
    "dev": [
        "yapf",
        "ipdb",
        "wheel",
        "isort",
        "flower",
        "ipython",
        "autoenv",
        "pygments",
        "autoflake",
        "virtualenv",
    ],
    "install": ["celery", "pyrabbit", "simplejson"],
}

if __name__ == "__main__":
    setup(
        name=PACKAGE,
        version=VERSION,
        license=LICENSE,
        description=DESC,
        long_description=DOC,
        author=AUTHOR,
        author_email=EMAIL,
        maintainer=AUTHOR,
        maintainer_email=EMAIL,
        url=URL,
        download_url=URL,
        keywords=KEYWORDS,
        platforms=PLATFORMS,
        classifiers=CLASSIFIERS,
        extras_require=REQUIRES,
        install_requires=REQUIRES["install"],
        include_package_data=True,
        packages=PACKAGES,
        scripts=SCRIPTS,
        zip_safe=False,
    )
