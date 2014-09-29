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
import pygubu


FILE_PATH = os.path.dirname(os.path.abspath(__file__))


class PreferencesUI(object):

    def __init__(self, master, translator=None):
        self.master = master
        self.translator = translator
        self.dialog = None
        self.modulestv = None
        self._create_preferences_dialog()

    def _create_preferences_dialog(self):
        builder = pygubu.Builder(self.translator)
        uifile = os.path.join(FILE_PATH, "ui/preferences_dialog.ui")
        builder.add_from_file(uifile)

        top = self.master.winfo_toplevel()
        self.dialog = dialog = builder.get_object('preferences', top)
        self.modulestv = builder.get_object('modules')

        builder.connect_callbacks(self)

    def on_btnclose_clicked(self):
        self.dialog.close()

    def on_pathremove_clicked(self):
        pass

    def on_pathadd_clicked(self):
        options = {
            'defaultextension': '.py',
            'filetypes': ((_('Python module'), '*.py'), (_('All'), '*.*'))}
        fname = filedialog.askopenfilename(**options)
        if fname:
            self.modulestv.insert('', tk.END, text=fname)
        
