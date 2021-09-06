#!/usr/bin/env python3
# encoding: UTF-8

"""Build tar.gz for pygubu

Needed packages to run (using Debian/Ubuntu package names):

    python3-tk
"""
import os

import pygubu

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = pygubu.__version__

_dirname_ = os.path.dirname(__file__)
readme_path = os.path.join(_dirname_, 'README.md')

setup(
    name='pygubu',
    version=VERSION,
    license='MIT',
    author='Alejandro Autalán',
    author_email='alejandroautalan@gmail.com',
    description='A tkinter GUI builder.',
    long_description=open(readme_path, 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/alejandroautalan/pygubu',

    packages=['pygubu', 'pygubu.builder',
              'pygubu.builder.widgets', 'pygubu.widgets'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Software Development :: User Interfaces",
    ],
)
