import os
try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
except:
    import Tkinter as tk
    import ttk
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
try:
    import ConfigParser as configparser
except:
    import configparser

from appdirs import AppDirs
import pygubu


FILE_PATH = os.path.dirname(os.path.abspath(__file__))
dirs = AppDirs('pygubu-designer')
CONFIG_FILE = os.path.join(dirs.user_data_dir, 'config')

CUSTOM_WIDGETS = 'CUSTOM_WIDGETS'
config = configparser.SafeConfigParser()
config.add_section(CUSTOM_WIDGETS)


def initialize_configfile():
    if not os.path.exists(dirs.user_data_dir):
        os.makedirs(dirs.user_data_dir)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

def save_configfile():
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def load_configfile():
    if not os.path.exists(CONFIG_FILE):
        initialize_configfile()
    else:
        config.read(CONFIG_FILE)

def get_custom_widgets():
    paths = []
    for k, p in config.items(CUSTOM_WIDGETS):
        paths.append(p)
    return paths

# Get user configuration
load_configfile()


class PreferencesUI(object):

    def __init__(self, master, translator=None):
        self.master = master
        self.translator = translator
        self.dialog = None
        self._create_preferences_dialog()
        self._load_options()

    def _create_preferences_dialog(self):
        builder = pygubu.Builder(self.translator)
        uifile = os.path.join(FILE_PATH, "ui/preferences_dialog.ui")
        builder.add_from_file(uifile)

        top = self.master.winfo_toplevel()
        self.dialog = dialog = builder.get_object('preferences', top)
        self.cwtv = builder.get_object('cwtv')
        self.path_remove = builder.get_object('path_remove')
        builder.connect_callbacks(self)
        
    def _load_options(self):
        for k, p in config.items(CUSTOM_WIDGETS):
            self.cwtv.insert('', 'end', text=p)
        self._configure_path_remove()

    def _save_options(self):
        config.remove_section(CUSTOM_WIDGETS)
        config.add_section(CUSTOM_WIDGETS)
        paths = []
        for iid in self.cwtv.get_children():
            txt = self.cwtv.item(iid, 'text')
            paths.append(txt)
        for j, p in enumerate(paths):
            config.set(CUSTOM_WIDGETS, 'w{0}'.format(j), p)
        save_configfile()

    def _configure_path_remove(self):
        if len(self.cwtv.get_children()):
            self.path_remove.configure(state='normal')
        else:
            self.path_remove.configure(state='disabled')
        
    def on_dialog_close(self, event=None):
        self._save_options()
        self.dialog.close()

    def on_pathremove_clicked(self):
        items = self.cwtv.selection()
        self.cwtv.delete(*items)
        self._configure_path_remove()

    def on_pathadd_clicked(self):
        options = {
            'defaultextension': '.py',
            'filetypes': ((_('Python module'), '*.py'), (_('All'), '*.*'))}
        fname = filedialog.askopenfilename(**options)
        if fname:
            self.cwtv.insert('', tk.END, text=fname)
            self._configure_path_remove()
        
