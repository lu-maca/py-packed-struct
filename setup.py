#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages

def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()

required_packages = [
    "bitstruct"
]

setup(
    name="py-packed-struct",
    version=0.1,
    author="Luca Macavero",
    author_email="luca.macavero@gmail.com",
    maintainer="Luca Macavero",
    maintainer_email="luca.macavero@gmail.com",
    url="",
    description="An implementation of C-like packed structures in Python",
    long_description=read("README.md"),
    python_requires=">=3.4",
    packages=find_packages(),
    setup_requires=["wheel"] + required_packages,
    install_requires=required_packages,
    include_package_data=True
)
