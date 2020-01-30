#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name = 'univisal',
    version="0.0.1",
    author="bluedrink9",
    description="universal vi emulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = find_packages(),
    url="https://github.com/bluedrink9/univisal",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)

