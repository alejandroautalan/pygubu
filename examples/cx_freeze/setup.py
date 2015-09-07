import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
	"packages": [
		"os", "tkinter",
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
	'include_files': ['button_cb.ui']
	}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "button_cb",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("button_cb.py", base=base)])
