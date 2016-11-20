# encoding: utf8
# setup.py
import sys
from distutils.core import setup
import py2exe

sys.argv.append("py2exe")

setup(
    console=["myapp.py"],
    data_files=[
        ("", ['myapp.ui']),
        ('imgs', [
            'imgs/MenuIcon4.gif',
            'imgs/ps_circle.gif',
            'imgs/ps_cross.gif',
            'imgs/ps_square.gif',
            'imgs/ps_triangle.gif',
            ])
        ],
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

