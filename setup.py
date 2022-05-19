#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


setup(
    name="img2cmap",
    version="0.2.2",
    license="MIT",
    description="Create colormaps from images",
    long_description="{}\n{}".format(
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub("", read("README.rst")),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Kevin Arvai",
    author_email="arvkevi@gmail.com",
    url="https://github.com/arvkevi/img2cmap",
    packages=find_packages("src", exclude=["tests*"]),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
    project_urls={
        "Documentation": "https://img2cmap.readthedocs.io/",
        "Changelog": "https://img2cmap.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://github.com/arvkevi/img2cmap/issues",
    },
    keywords=[
        "matplotlib",
        "colormap",
        "image",
    ],
    python_requires=">=3.6",
    install_requires=[
        "matplotlib",
        "scikit-learn",
        "numpy",
        "pillow",
        "kneed",
    ],
    extras_require={
        "dev": [
            "black",
        ],
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
)
