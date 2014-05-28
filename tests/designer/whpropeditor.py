# encoding: utf8
from __future__ import unicode_literals
from __future__ import print_function

import os
import sys

cur_dir = os.path.abspath(os.path.dirname(__file__))
pygubu_basedir = os.path.abspath(os.path.join(cur_dir, './../..'))

if pygubu_basedir not in sys.path:
    sys.path.insert(0, pygubu_basedir)

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubudesigner.widgets import WHPropertyEditor

if __name__ == '__main__':
    root = tk.Tk()
    editor = WHPropertyEditor(root)
    editor.grid()
    editor.edit('320|240')

    def see_var(event=None):
        print(editor.value)

    editor.bind('<<PropertyChanged>>', see_var)
    root.mainloop()
