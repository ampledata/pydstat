#!/usr/bin/env python
"""Setup for pydstat.

Source:: https://github.com/ampledata/pydstat
"""

__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


import setuptools


def read_readme():
    """Reads in README file for use in setuptools."""
    with open('README.rst') as rmf:
        rmf.read()


setuptools.setup(
    name='pydstat',
    version='1.0.1',
    description='A Pythonic Wrapper for pidstat.',
    long_description=read_readme(),
    author='Greg Albrecht',
    author_email='gba@splunk.com',
    url='https://github.com/ampledata/pydstat',
    license='Apache License 2.0',
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    setup_requires=['nose'],
    tests_require=['nose', 'mock', 'coverage'],
    test_suite='tests',
    entry_points={'console_scripts': ['pydstat = pydstat.cmd:main']}
)
