# encoding: utf-8
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog


class PathChooserInput(ttk.Frame):
    """Allows to choose a file or directory.

    Encapsulates the usage of the functions:

        filedialog.askopenfilename()
        filedialog.asksaveasfilename(**fdoptions)
        filedialog.askdirectory()

    Generates <<PathChooserPathChanged>> event when the path is changed.

    Dialog options:
      initialdir: str
      filetypes: iterable
      title: str
      mustexist: bool
      defaultextension: str

    Usage Example:
        # Choose filename for open:
        pcifile = PathChooserInput(framex)
        pcifile.config(
            initialdir='/home',
            title='Open file:',
            type='file',
            filetypes=[('text files-', '.txt'), ('uifiles', '.ui')]
            )
        pcifile.pack(fill='x', side='top')

        # Choose filename for save:
        pcofile = PathChooserInput(framex)
        pcofile.config(
            initialdir='/home',
            title='Save to:',
            type='file',
            mustexist=False,
            defaultextension=".txt",
            )
        pcofile.pack(fill='x', side='top')

        # Choose directory:
        pcidir = PathChooserInput(framex)
        pcidir.config(initialdir='/usr/local', mustexist=True,
                      title='Choose a directory:', type='directory')
        pcidir.pack(fill='x', side='top')
    """

    FILE = "file"
    DIR = "directory"

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._choose = self.FILE
        self._oldvalue = ""
        self._state = "normal"
        self._fdoptions = {
            "filetypes": tuple(),
            "initialdir": None,
            "mustexist": True,
            "title": None,
            "defaultextension": None,
        }
        # subwidgets
        self.entry = o = ttk.Entry(self, state=self._state)
        o.grid(row=0, column=0, sticky="ew")
        o.bind("<KeyPress>", self.__on_enter_key_pressed)
        o.bind("<FocusOut>", self.__on_focus_out)
        self.folder_button = o = ttk.Button(
            self,
            text="▶",
            command=self.__on_folder_btn_pressed,
            width=4,
            state=self._state,
        )
        o.grid(row=0, column=1, padx=2)

        # self.rowconfigure(0, weight = 0)
        self.columnconfigure(0, weight=1)

    def configure(self, cnf=None, **kw):
        if cnf:
            return super().configure(cnf, **kw)
        key = "type"
        if key in kw:
            self._choose = kw.pop(key)
        key = "image"
        if key in kw:
            self.folder_button.configure(image=kw.pop(key))
        key = "path"
        if key in kw:
            self.entry.delete(0, "end")
            self.entry.insert(0, kw.pop(key))
            self._generate_changed_event()
        key = "textvariable"
        if key in kw:
            self.entry.configure(textvariable=kw.pop(key))
            self._generate_changed_event()
        key = "state"
        if key in kw:
            value = kw.pop(key)
            self.entry.config(state=value)
            if value in ("disabled", "readonly"):
                self.folder_button.config(state="disabled")
            else:
                self.folder_button.config(state=value)
        # dialog options
        for key in tuple(kw.keys()):
            if key in self._fdoptions:
                self._fdoptions[key] = kw.pop(key)
        return super().configure(cnf, **kw)

    config = configure

    def cget(self, key):
        option = "type"
        if key == option:
            return self._choose
        option = "image"
        if key == option:
            return self.folder_button.cget(key)
        option = "path"
        if key == option:
            return self.entry.get()
        option = "textvariable"
        if key == option:
            return self.entry.cget(option)
        option = "state"
        if key == option:
            return self.entry.cget(option)
        # dialog options
        if key in self._fdoptions:
            return self._fdoptions[key]
        return super().cget(key)

    __getitem__ = cget

    def _is_changed(self):
        if self._oldvalue != self.entry.get():
            return True
        return False

    def _generate_changed_event(self):
        if self._is_changed():
            self._oldvalue = self.entry.get()
            self.event_generate("<<PathChooserPathChanged>>")

    def __on_enter_key_pressed(self, event):
        key = event.keysym
        if key in ("Return", "KP_Enter"):
            self._generate_changed_event()

    def __on_focus_out(self, event):
        self._generate_changed_event()

    def __on_folder_btn_pressed(self):
        fname = None
        fdoptions = self._fdoptions.copy()
        fdoptions["parent"] = self.winfo_toplevel()
        if fdoptions["initialdir"] is None:
            fdoptions["initialdir"] = self.cget("path")
        if self._choose == self.FILE:
            must_exists = fdoptions.pop("mustexist")
            if must_exists:
                fname = filedialog.askopenfilename(**fdoptions)
            else:
                fname = filedialog.asksaveasfilename(**fdoptions)
        else:
            fdoptions.pop("filetypes")
            fdoptions.pop("defaultextension")
            fname = filedialog.askdirectory(**fdoptions)
        if fname:
            self.configure(path=fname)
