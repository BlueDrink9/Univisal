#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name = 'univisal',
    version="0.0.1",
    author="bluedrink9",
    description="universal vi emulation",
    # entry_points={
    #
    #     "univisal-autokey": "adapters/autokey/...",
    # },
    entry_points = {
        'console_scripts': ['univisal=src.univisal.__main__:main'],
    },
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
    # install_requires=[
    #     'Enum',
    #     ],
    tests_require=[
        "pytest",
    ],
    test_suite="pytest",
    python_requires='>=3',
)

