#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

from os import path
from setuptools import setup, find_packages


def local_scheme(version):
    """
    Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI
    """
    return ""


if __name__ == "__main__":
    HERE = path.abspath(path.dirname(__file__))

    with open(path.join(HERE, "README.rst"), encoding="utf-8") as readme:
        LONG_DESCRIPTION = readme.read()

    setup(
        long_description=LONG_DESCRIPTION,
        packages=find_packages(exclude=["docs", "test_project"]),
        include_package_data=True,
        zip_safe=False,
        use_scm_version={"local_scheme": local_scheme},
    )
