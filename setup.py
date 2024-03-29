# -*- coding: utf-8 -*-
"""Setup file for numpwdata
"""
__author__ = ""
__version__ = ""

from os import path

from setuptools import setup, find_packages

CWD = path.abspath(path.dirname(__file__))

with open(path.join(CWD, "README.md"), encoding="utf-8") as inp:
    LONG_DESCRIPTION = inp.read()

with open(path.join(CWD, "requirements.txt"), encoding="utf-8") as inp:
    REQUIREMENTS = [el.strip() for el in inp.read().split(",")]

setup(
    name="numpwdata",
    version=__version__,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=__author__,
    keywords=[],
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    entry_points={"console_scripts": ["numpwdata=numpwdata.manage:main"]},
)
