#!/usr/bin/env python3
# encoding: UTF-8

"""Build tar.gz for pygubu

Needed packages to run (using Debian/Ubuntu package names):

    python3-tk
"""

import sys
import os
import shutil
import platform
import pygubu

VERSION = pygubu.__version__

with_setuptools = False
if 'USE_SETUPTOOLS' in os.environ or 'pip' in __file__:
    try:
        from setuptools.command.install import install
        from setuptools import setup
        with_setuptools = True
    except:
        with_setuptools = False

if with_setuptools is False:
    from distutils.command.install import install
    from distutils.core import setup


class CustomInstall(install):
    """Custom installation class on package files.
    """

    def run(self):
        """Run parent install, and then save the install dir in the script."""
        install.run(self)

        #
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

            if platform.system() == 'Windows':
                dest = script_path + '.py'
                shutil.move(script_path, dest)
        #
        # Remove old pygubu.py from scripts path if exists
        spath = os.path.join(self.install_scripts, 'pygubu')
        for ext in ('.py', '.pyw'):
            filename = spath + ext
            if os.path.exists(filename):
                os.remove(filename)
        #
        # Create .bat file on windows
        if platform.system() == 'Windows':
            pdpath = os.path.join(self.install_scripts, 'pygubu-designer.py')
            batpath = os.path.join(self.install_scripts,
                                    'pygubu-designer.bat')
            with open(batpath, 'w') as batfile:
                content = "{0} {1}".format(sys.executable, pdpath)
                batfile.write(content)


long_description = \
"""
Welcome to pygubu a GUI designer for tkinter
============================================

Pygubu is a RAD tool to enable quick & easy development of user interfaces
for the python tkinter module.

The user interfaces designed are saved as XML, and by using the pygubu builder
these can be loaded by applications dynamically as needed.
Pygubu is inspired by Glade.


Installation
------------

Pygubu requires python >= 2.7 (Tested only in python 2.7.3 and 3.2.3
with tk8.5)

Download and extract the tarball. Open a console in the extraction
path and execute:

::

    python setup.py install


Usage
-----

Create an UI definition using pygubu and save it to a file. Then, create
your aplication script as shown below:

::

    #test.py
    import tkinter as tk
    import pygubu

    class Application:
        def __init__(self, master):

            #1: Create a builder
            self.builder = builder = pugubu.Builder()

            #2: Load an ui file
            builder.add_from_file('test.ui')

            #3: Create the widget using a master as parent
            self.mainwindow = builder.get_object('mainwindow', master)

    if __name__ == '__main__':
        root = tk.Tk()
        app = Application(root)
        root.mainloop()


See the examples directory or watch this hello world example on
video http://youtu.be/wuzV9P8geDg
"""
setup(
    name='pygubu',
    version=VERSION,
    license='GPL-3',
    author='Alejandro Autalán',
    author_email='alejandroautalan@gmail.com',
    description='A tkinter GUI builder.',
    long_description=long_description,
    url='https://github.com/alejandroautalan/pygubu',

    packages=['pygubu', 'pygubu.builder', 'pygubu.builder.widgets',
        'pygubu.widgets', 'pygubudesigner', 'pygubudesigner.util',
        'pygubudesigner.widgets'],
    package_data={
        'pygubudesigner': [
            'images/*.gif', 'images/widgets/*/*.gif',
            'ui/*.ui',
            'locale/*/*/*.mo'],
    },
    scripts=["bin/pygubu-designer"],
    cmdclass={
        'install': CustomInstall,
    },
    install_requires=['appdirs>=1.3'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Software Development :: User Interfaces",
    ],
)
