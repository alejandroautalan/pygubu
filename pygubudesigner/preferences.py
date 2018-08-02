# encoding: utf-8
import os
import sys
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

options = {
    'widget_set': {'values': '["tk", "ttk"]', 'default':'ttk'},
    'widget_palette': {'values': '["accordion", "treeview"]', 'default':'accordion'}
}

SEC_GENERAL = 'GENERAL'
SEC_CUSTOM_WIDGETS = 'CUSTOM_WIDGETS'
config = configparser.SafeConfigParser()
config.add_section(SEC_CUSTOM_WIDGETS)
config.add_section(SEC_GENERAL)


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
    defaults = {}
    for k in options:
        defaults[k] = options[k]['default']
    if sys.version_info < (3,0):
        #Python 2.7
        keys = defaults.keys()
        for i in range(0, len(defaults)):
            config.set(SEC_GENERAL, keys[i], defaults.get(keys[i]))
    else:
        #Python 3
        config[SEC_GENERAL] = defaults
    if not os.path.exists(CONFIG_FILE):
        initialize_configfile()
    else:
        config.read(CONFIG_FILE)

def get_custom_widgets():
    paths = []
    for k, p in config.items(SEC_CUSTOM_WIDGETS):
        paths.append(p)
    return paths
    
def get_option(key):
    return config.get(SEC_GENERAL, key)

# Get user configuration
load_configfile()


class PreferencesUI(object):

    def __init__(self, master, translator=None):
        self.master = master
        self.translator = translator
        self.dialog = None
        self.builder = None
        self._create_preferences_dialog()
        self._load_options()

    def _create_preferences_dialog(self):
        self.builder = builder = pygubu.Builder(self.translator)
        uifile = os.path.join(FILE_PATH, "ui/preferences_dialog.ui")
        builder.add_from_file(uifile)

        top = self.master.winfo_toplevel()
        self.dialog = dialog = builder.get_object('preferences', top)
        
        #General
        for key in ('widget_set', 'widget_palette'):
            cbox = builder.get_object(key)
            cbox.configure(values=options[key]['values'])
        
        #Custom widgets
        self.cwtv = builder.get_object('cwtv')
        self.path_remove = builder.get_object('path_remove')
        builder.connect_callbacks(self)
        
    def _load_options(self):
        # General
        for key in options:
            var = self.builder.get_variable(key)
            var.set(get_option(key))
        # Custom widgets
        for k, p in config.items(SEC_CUSTOM_WIDGETS):
            self.cwtv.insert('', 'end', text=p)
        self._configure_path_remove()

    def _save_options(self):
        # General
        for key in options:
            var = self.builder.get_variable(key)
            config.set(SEC_GENERAL, key, var.get())
        # Custom Widgets
        config.remove_section(SEC_CUSTOM_WIDGETS)
        config.add_section(SEC_CUSTOM_WIDGETS)
        paths = []
        for iid in self.cwtv.get_children():
            txt = self.cwtv.item(iid, 'text')
            paths.append(txt)
        for j, p in enumerate(paths):
            config.set(SEC_CUSTOM_WIDGETS, 'w{0}'.format(j), p)
        save_configfile()
        self.master.event_generate('<<PygubuDesignerPreferencesSaved>>')

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
        
