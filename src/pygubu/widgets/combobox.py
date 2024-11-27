# encoding: utf-8
import json
import tkinter as tk
import tkinter.ttk as ttk
from collections import OrderedDict


class Combobox(ttk.Combobox):
    """
    A ttk.Combobox that accepts a list of (key, label) pair of options.
    """

    def __init__(self, *args, keyvariable=None, textvariable=None, **kw):
        self._keyvarcb = None
        self._txtvarcb = None
        self._choices = OrderedDict()
        self._keyvar = tk.StringVar() if keyvariable is None else keyvariable
        self._txtvar = tk.StringVar() if textvariable is None else textvariable

        key = "values"
        if key in kw:
            values = kw[key]
            self.choices = values
            values = self.__choices2tkvalues(self.choices)
            kw[key] = values

        # only normal/disabled supported
        # normal is converted to readonly
        key = "state"
        state = kw.get(key, "readonly")
        if state not in ("readonly", "disabled"):
            state = "readonly"
        kw[key] = state
        kw["textvariable"] = self._txtvar

        super().__init__(*args, **kw)

        self.__config_keyvar(self._keyvar)
        self.__config_txtvar(self._txtvar)

    def __config_keyvar(self, var):
        if var is None:
            return

        def on_keyvar_changed(varname, elementname, mode):
            nvalue = self._keyvar.get()
            if nvalue in self._choices:
                self.current(nvalue)

        keyvar = self._keyvar
        if self._keyvarcb is not None:
            keyvar.trace_remove("write", self._keyvarcb)
        self._keyvar = var
        self._keyvarcb = var.trace_add("write", on_keyvar_changed)

    def __config_txtvar(self, var):
        keyvar = self._keyvar
        if var is None or keyvar is None:
            return

        def on_txtvar_changed(varname, elementname, mode):
            ckey = self.current()
            if ckey is not None:
                self._keyvar.set(ckey)

        txtvar = self._txtvar
        if txtvar and self._txtvarcb is not None:
            txtvar.trace_remove("write", self._txtvarcb)
        self._txtvar = var
        self._txtvarcb = var.trace_add("write", on_txtvar_changed)

    def _delayed_clear_vars(self):
        # clear variables:
        self._clear_tkvar(self._keyvar)
        self._clear_tkvar(self._txtvar)

    def _clear_tkvar(self, variable):
        if isinstance(variable, tk.StringVar):
            variable.set("")

    def configure(self, cnf=None, **kw):
        if cnf:
            return super().configure(cnf, **kw)
        key = "values"
        if key in kw:
            self.choices = kw[key]
            kw[key] = self.__choices2tkvalues(self.choices)
            # clear vars after setting values
            self.after_idle(self._delayed_clear_vars)
        key = "keyvariable"
        if key in kw:
            value = kw.pop(key)
            self.__config_keyvar(value)
        key = "textvariable"
        if key in kw:
            value = kw[key]
            self.__config_txtvar(value)

        # only readonly and disabled supported
        key = "state"
        if key in kw:
            state = kw.get(key, "readonly")
            if state not in ("readonly", "disabled"):
                state = "readonly"
            kw[key] = state
        return super().configure(cnf, **kw)

    config = configure

    def cget(self, key):
        option = "values"
        if key == option:
            return json.dumps(self.choices)
        option = "keyvariable"
        if key == option:
            return self._keyvar
        option = "textvariable"
        if key == option:
            return self._txtvar
        return super().cget(key)

    def __obj2choices(self, values):
        """
        - json list of key, value pairs:
            Example: [["A", "Option 1 Label"], ["B", "Option 2 Label"]]
        - space separated string with a list of options:
            Example: "Option1 Opt2 Opt3"
            will be converted to a key, value pair of the following form:
            (("Option1", "Option1), ("Opt2", "Opt2"), ("Opt3", "Opt3"))
        - an iterable of key, value pairs
        """
        choices = values
        # choices from string
        if isinstance(values, type("")):
            obj = None
            # try json string
            try:
                obj = json.loads(values)
            except ValueError:
                obj = values
            if isinstance(obj, type([])):
                choices = obj
            else:
                choices = obj.split()
        return choices

    def __choices2tkvalues(self, choices):
        """choices: iterable of key, value pairs"""
        values = []
        for k, v in choices:
            values.append(v)
        return values

    @property
    def choices(self):
        return tuple(self._choices.items())

    @choices.setter
    def choices(self, values):
        values = self.__obj2choices(values)
        self._choices.clear()
        for idx, v in enumerate(values):
            key = value = v
            if not isinstance(v, type("")) and len(v) == 2:
                key, value = v
            self._choices[key] = value

    def current(self, key=None):
        """Get the index of the current selection.
        If key is given, return the index of the key.
        """
        idx = super().current(None)
        index = -1
        ckey = None
        # find the key of the current selection,
        # or if a key was given, its index
        for i, k in enumerate(self._choices.keys()):
            if key is None and idx == i:
                ckey = k
                break
            elif key == k:
                index = i
                break
        if key is None:
            # return current key
            return ckey
        return super().current(index)

    def set(self, key):
        value = self._choices[key]
        return super().set(value)

    def get(self):
        return self.current()


if __name__ == "__main__":

    def show_selection(event):
        cbox = event.widget
        print("values:", cbox.cget("values"))
        print("current:", cbox.current())
        var = cbox.cget("keyvariable")
        print("keyvar: ", var.get())
        var = cbox.cget("textvariable")
        print("textvar: ", var.get())

    root = tk.Tk()
    txtvalues = '[["DNI", "Doc.Nac.Id."], ["LE", "Libreta Enrolamientox"]]'
    c = Combobox(root, values=txtvalues)
    c.bind("<<ComboboxSelected>>", show_selection)
    c.configure(values=txtvalues)
    c.set("LE")
    c.grid()

    values = (("tres", 3), (4, "cuatro"), (6, "seis"))
    c = Combobox(root, values=values)
    c.bind("<<ComboboxSelected>>", show_selection)
    c.set(6)
    c.grid()

    var = tk.StringVar()
    var.set("C")
    e = ttk.Entry(root, textvariable=var)
    e.grid()

    var2 = tk.StringVar()
    e2 = ttk.Entry(root, textvariable=var2)
    e2.grid()

    values = (
        ("", "Seleccione Opción"),
        ("A", "A label"),
        ("B", "B label"),
        ("C", "C label"),
    )
    c = Combobox(root, textvariable=var)
    c.bind("<<ComboboxSelected>>", show_selection)
    c.configure(values=values)
    c.set("")
    c.grid()

    c.configure(keyvariable=var2)
    var2.set("A")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
