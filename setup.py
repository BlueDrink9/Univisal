#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name = 'univisal',
    version="0.0.1",
    author="bluedrink9",
    description="universal vi emulation",
    install_requires=[
        'enum34;python_version<"3.4"',
        'aenum;python_version<"3.6"',
    ],
    # entry_points={
    #
    #     "univisal-autokey": "adapters/autokey/...",
    # },
    keywords="vi-emulator vi emulator windows Xorg linux X11 OSX Mac",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = find_packages("src"),
    url="https://github.com/bluedrink9/univisal",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    include_package_data=True,
    setup_requires=["pytest-runner"],
    tests_require=[
        "pytest",
        "pytest-cov",
    ],
    test_suite="pytest",
    python_requires='>=3',
)

