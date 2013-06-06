#!/usr/bin/env python3
# encoding: UTF-8

"""Build tar.gz for pygubu

Needed packages to run (using Debian/Ubuntu package names):

    python3-tk
"""

import os
import shutil

from distutils.command.install import install
from distutils.core import setup

VERSION = open('version.txt').read().strip()


class CustomInstall(install):
    """Custom installation class on package files.
    """

    def run(self):
        """Run parent install, and then save the install dir in the script."""
        install.run(self)

        # fix installation path in the script(s)
        for script in self.distribution.scripts:
            script_path = os.path.join(self.install_scripts,
                                       os.path.basename(script))

            with open(script_path) as fh:
                content = fh.read()

            ipath = os.path.abspath(self.install_lib)
            content = content.replace('@ INSTALLED_BASE_DIR @', ipath)

            with open(script_path, 'w') as fh:
                fh.write(content)


setup(
    name='pygubu',
    version=VERSION,
    license='GPL-3',
    author='Alejandro Autalán',
    author_email='alejandroautalan@gmail.com',
    description='A tkinter GUI builder.',
    long_description='A tkinter GUI builder.',
    url='https://github.com/alejandroautalan/pygubu',

    packages=['pygubu', 'pygubu.builder', 'pygubu.builder.widgets',
        'pygubu.uidesigner', 'pygubu.uidesigner.util', 'pygubu.widgets'],
    package_data={
        'pygubu.uidesigner': [
            'images/*.gif', 'images/widgets/16x16/*.gif',
            'images/widgets/22x22/*.gif', 'ui/*.ui',
            'locale/*/*/*.mo'],
    },
    scripts=["bin/pygubu"],
    cmdclass={
        'install': CustomInstall,
    },
)
