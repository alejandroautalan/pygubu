[Leer en español] (LEEME.md)

Welcome to Pygubu!
============================================

`Pygubu` is a [RAD tool](https://en.wikipedia.org/wiki/Rapid_application_development) to enable quick and easy development of user interfaces for the Python's `tkinter` module.

The user interfaces designed are saved as [XML](https://en.wikipedia.org/wiki/XML) files, and, by using the _pygubu builder_, these can be loaded by applications dynamically as needed.

Pygubu is inspired by [Glade](https://glade.gnome.org).

Installation
====

Pygubu requires Python >= 2.7 (Tested only in Python 2.7.3 and 3.2.3 with tk8.5).

You can install pygubu using:

### zip tarball

Download and extract the [tarball](http://searchenterpriselinux.techtarget.com/definition/tarball). Open a console in the extraction path and execute:

```
python setup.py install
```

### pip

```
pip install pygubu
```

Note that if you are using a Python 3 version, you might want to use its `pip` tool, for example:

    pip3.5 install pygubu
    
In the previous case, I am using the `pip` tool of Python 3.5.  


To check that the installation was successful, you can try to import `pygubu` (for example from the [IDLE](https://en.wikipedia.org/wiki/IDLE_(Python)))

    import pygubu
    
If you have no `ImportError`, then your installation was successful.

Usage
=====

Type on the terminal one of the following commands depending on your system.

### Unix-like systems

```
pygubu-designer
```

### Windows

```
C:\Python34\Scripts\pygubu-designer.bat
```

Where `C:\Python34` is the path to **your** Python installation directory.


The following _pygubu-designer_ interface should appear:

[]()

Create an UI definition using **pygubu-designer** and save it to a file.

[helloworld.ui] (examples/helloworld.ui)

Then, create your aplication script as shown below:

```python
#test.py
try:
    import tkinter as tk
except:
    import Tkinter as tk
import pygubu


class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('helloworld.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', master)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
```

Documentation
=============

Visit the pygubu [wiki](https://github.com/alejandroautalan/pygubu/wiki) for more documentation.

An excellent tkinter reference is available [here](http://www.nmt.edu/tcc/help/pubs/tkinter/web/index.html).

See the examples directory or watch this hello world example on [video](http://youtu.be/wuzV9P8geDg)


History
=======

Changes for version 0.9.6.7

  * Remove old pygubu.py script for old installations.
    Create pybugu-designer.bat file for windows platform. Fixes #38

Changes for version 0.9.6.6

  * Fixed bug: color value setting to None when presing Cancel on color selector.
  * Add '.png' format to Stockimage if tk version support it. fixes #36
  * Minor changes to main UI.

Changes for version 0.9.6.5

  * Fixed bug on menu creation.
  * Fixed issues #14 and #22
  * Added helper method to avoid call get_variable for every variable. refs #29

Changes for version 0.9.6.4

  * Fixed bug #33 "Wrong textvariable format when create ui file"

Changes for version 0.9.6.3

  * Use old menu preview on platforms other than linux  (new preview does not work on windows)

Changes for version 0.9.6.2

  * Property editors rewritten from scratch
  * Improved menu preview
  * Added font property editor
  * Fixed menu issues

Changes for version 0.9.5.1

  * Add select hotkey to widget tree. (i - select previous item, k - select next item)
  * Copied menu example from wiki to examples folder.

Changes for version 0.9.5

  * Renamed designer startup script to pygubu-designer (see [#20](/../../issues/20))
  * Fixed bugs.

Changes for version 0.9.4

  * Added Toplevel widget
  * Added generic Dialog widget
  * Rewrited scrolledframe widget internals, ideas and code taken from tkinter wiki.
  * Added more widget icons.
  * Fixed bugs.

Changes for version 0.9.3
    
  * Allow to select control variable type
  * Fixed some bugs.

Changes for version 0.9.2

  * Added more wiki pages.
  * Fixed issues #3, #4

Changes for version 0.9.1

  * Separate designer module from main package
  * Added menu to select current ttk theme
  * Fix color selector issues.

Changes for version 0.9

  * Add validator for pax and pady properties.
  * Improved ScrolledFrame widget.
  * Added more wiget icons.
  * Fix cursor type on preview panel.

Changes for version 0.8

  * Added translation support
  * Translated pygubu designer to Spanish

Changes for version 0.7

  * Added python 2.7 support
  * Added initial TkApplication class
  * Fixed some bugs.

First public version 0.6
