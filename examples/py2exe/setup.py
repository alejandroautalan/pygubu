# setup.py
import sys
from distutils.core import setup
import py2exe

sys.argv.append("py2exe")

setup(
    console=["button_cb.py"],
    data_files=[("", ["button_cb.ui"])],
    options= {
        "py2exe": { 
            "includes" : ["pygubu.builder.tkstdwidgets",
                          "pygubu.builder.ttkstdwidgets",
                          "pygubu.builder.widgets.dialog",
                          "pygubu.builder.widgets.editabletreeview",
                          "pygubu.builder.widgets.scrollbarhelper",
                          "pygubu.builder.widgets.scrolledframe",
                          "pygubu.builder.widgets.tkscrollbarhelper",
                          "pygubu.builder.widgets.tkscrolledframe",
                          "pygubu.builder.widgets.pathchooserinput",]
                    }},
        )

