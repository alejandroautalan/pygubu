#!/usr/bin/env python3
# encoding: UTF-8

"""Build tar.gz for pygubu

Needed packages to run (using Debian/Ubuntu package names):

    python3-tk
"""
import pathlib
from io import open

import pygubu

from setuptools import setup, find_packages

VERSION = pygubu.__version__

_dirname_ = pathlib.Path(__file__).parent
readme_path = _dirname_ / "README.md"
extras_require = {
    "ttkwidgets": {"ttkwidgets"},
    "tksheet": {"tksheet"},
    "tkinterweb": {"tkinterweb"},
    "tkintertable": {"tkintertable"},
    "tkcalendar": {"tkcalendar"},
    "AwesomeTkinter": {"AwesomeTkinter"},
    "awesometkinter": {"AwesomeTkinter"},
    "all": {
        "AwesomeTkinter",
        "tkcalendar",
        "tkintertable",
        "tkinterweb",
        "tksheet",
        "ttkwidgets",
    },
}

setup(
    name="pygubu",
    version=VERSION,
    license="MIT",
    author="Alejandro Autalán",
    author_email="alejandroautalan@gmail.com",
    description="A tkinter GUI builder.",
    long_description=open(readme_path, "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alejandroautalan/pygubu",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.6",
    extras_require=extras_require,
)
