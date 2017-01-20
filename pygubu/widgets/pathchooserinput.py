# encoding: utf8
from __future__ import unicode_literals

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
except:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog


class PathChooserInput(ttk.Frame):
    """ Allows to choose a file or directory.
    
    Generates <<PathChooserPathChanged>> event when the path is changed.
    
    """

    FILE = 'file'
    DIR = 'directory'

    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        self._choose = self.FILE
        self._oldvalue = ''
        # subwidgets
        self.entry = o = ttk.Entry(self)
        o.grid(row=0, column=0, sticky='ew')
        o.bind('<KeyPress>', self.__on_enter_key_pressed)
        o.bind('<FocusOut>', self.__on_focus_out)
        self.folder_button = o = ttk.Button(self, text='▶', command = self.__on_folder_btn_pressed, width=4)
        o.grid(row=0, column=1, padx=2)

        #self.rowconfigure(0, weight = 0)
        self.columnconfigure(0, weight = 1)

    def configure(self, cnf=None, **kw):
        args = tk._cnfmerge((cnf, kw))
        key = 'type'
        if key in args:
            self._choose = args[key]
            del args[key]
        key = 'image'
        if key in args:
            self.folder_button.configure(image=args[key])
            del args[key]
        key = 'path'
        if key in args:
            self.entry.delete(0, 'end')
            self.entry.insert(0, args[key])
            self._generate_changed_event()
            del args[key]
        key = 'textvariable'
        if key in args:
            self.entry.configure(textvariable=args[key])
            self._generate_changed_event()
            del args[key]
        ttk.Frame.configure(self, args)

    config = configure

    def cget(self, key):
        option = 'type'
        if key == option:
            return self._choose
        option = 'image'
        if key == option:
            return self.folder_button.cget(key)
        option = 'path'
        if key == option:
            return self.entry.get()
        option = 'textvariable'
        if key == option:
            return self.entry.cget(option)
        return ttk.Frame.cget(self, key)

    __getitem__ = cget
        
    def _is_changed(self):
#        print(repr(self._oldvalue), ':', repr(self.entry.get()))
        if self._oldvalue != self.entry.get():
            return True
        return False
    
    def _generate_changed_event(self):
        if self._is_changed():
            self._oldvalue = self.entry.get()
            self.event_generate('<<PathChooserPathChanged>>')

    def __on_enter_key_pressed(self, event):
        key = event.keysym
        if key in  ('Return','KP_Enter'):
            self._generate_changed_event()
    
    def __on_focus_out(self, event):
         self._generate_changed_event()

    def __on_folder_btn_pressed(self):
        fname = None
        if self._choose == self.FILE:
            fname = filedialog.askopenfilename(initialdir=self.cget('path'))
        else:
            fname = filedialog.askdirectory(initialdir=self.cget('path'))
        if fname:
            self.configure(path=fname)

