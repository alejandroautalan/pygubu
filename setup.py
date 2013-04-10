#!/usr/bin/env python3


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

            content = content.replace('@ INSTALLED_BASE_DIR @',
                                      self.install_lib)

            with open(script_path, 'w') as fh:
                fh.write(content)

        # version file
        shutil.copy("version.txt", self.install_lib)


setup(
    name='pygubu',
    version=VERSION,
    license='GPL-3',
    author='Alejandro Autalán',
    author_email='alejandroautalan@gmail.com',
    description='A tkinter GUI builder.',
    long_description='A tkinter GUI builder.',
    url='https://github.com/alejandroautalan/pygubu',

    packages=["pygubu", "pygubu.uidesigner", "pygubu.uidesigner.util",
        'pygubu.widgets'],
    package_data={
        'pugubu': ['../version.txt'],
        'pygubu.uidesigner': ['images/*.gif', 'ui/*.ui'],
        '' : ['version.txt'],
    },
    scripts=["bin/pygubu"],
    cmdclass={
        'install': CustomInstall,
    },
)
