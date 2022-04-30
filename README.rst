========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/img2cmap/badge/?style=flat
    :target: https://img2cmap.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/arvkevi/img2cmap/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/arvkevi/img2cmap/actions

.. |requires| image:: https://requires.io/github/arvkevi/img2cmap/requirements.svg?branch=main
    :alt: Requirements Status
    :target: https://requires.io/github/arvkevi/img2cmap/requirements/?branch=main

.. |codecov| image:: https://codecov.io/gh/arvkevi/img2cmap/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/arvkevi/img2cmap

.. |version| image:: https://img.shields.io/pypi/v/img2cmap.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/img2cmap

.. |wheel| image:: https://img.shields.io/pypi/wheel/img2cmap.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/img2cmap

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/img2cmap.svg
    :alt: Supported versions
    :target: https://pypi.org/project/img2cmap

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/img2cmap.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/img2cmap

.. |commits-since| image:: https://img.shields.io/github/commits-since/arvkevi/img2cmap/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/arvkevi/img2cmap/compare/v0.0.0...main



.. end-badges

Create colormaps from images

* Free software: MIT license

Installation
============

::

    pip install img2cmap

You can also install the in-development version with::

    pip install https://github.com/arvkevi/img2cmap/archive/main.zip


Documentation
=============


https://img2cmap.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
