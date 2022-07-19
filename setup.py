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


def get_extra_requires(path, add_all=True):
    import re
    from collections import defaultdict

    with open(path) as fp:
        extra_deps = defaultdict(set)
        for k in fp:
            if k.strip() and not k.startswith("#"):
                tags = set()
                if ":" in k:
                    k, v = k.split(":")
                    tags.update(vv.strip() for vv in v.split(","))
                tags.add(re.split("[<=>]", k)[0])
                for t in tags:
                    extra_deps[t].add(k)

        # add tag `all` at the end
        if add_all:
            extra_deps["all"] = set(vv for v in extra_deps.values() for vv in v)

    return extra_deps


_dirname_ = pathlib.Path(__file__).parent
readme_path = _dirname_ / "README.md"
extra_req_path = _dirname_ / "extra_requirements.txt"

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
    extras_require=get_extra_requires(extra_req_path),
)
