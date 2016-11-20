# encoding: utf8
import sys
from cx_Freeze import setup, Executable

# Note: I'm using cx_freeze on python 2.7,
#       change tkinter module names when using python3

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
	"packages": [
		"os", "Tkinter", 'tkMessageBox', 'ttk',
		# Pygubu packages:
		"pygubu.builder.tkstdwidgets",
		"pygubu.builder.ttkstdwidgets",
		"pygubu.builder.widgets.dialog",
		"pygubu.builder.widgets.editabletreeview",
		"pygubu.builder.widgets.scrollbarhelper",
		"pygubu.builder.widgets.scrolledframe",
		"pygubu.builder.widgets.tkscrollbarhelper",
		"pygubu.builder.widgets.tkscrolledframe",
		"pygubu.builder.widgets.pathchooserinput"],
	'include_files': ['myapp.ui', 'imgs']
	}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "myapp",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("myapp.py", base=base)])
