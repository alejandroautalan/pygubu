# encoding: utf8

from collections import OrderedDict
import json
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


class Combobox(ttk.Combobox):
    """
    A ttk.Combobox that accepts a list of (key, label) pair of options.
    """
    def __init__(self, master=None, **kw):
        self._choices = OrderedDict()
        key = 'values'
        if key in kw:
            values = kw[key]
            self.choices = values
            values = self.__choices2tkvalues(self.choices)
            kw[key] = values
        kw['state'] = 'readonly'
        ttk.Combobox.__init__(self, master, **kw)
    
    def configure(self, cnf=None, **kw):
        args = tk._cnfmerge((cnf, kw))
        key = 'values'
        if key in args:
            self.choices = args[key]
            args[key] = self.__choices2tkvalues(self.choices)
        ttk.Combobox.configure(self, args)

    config = configure

    def cget(self, key):
        option = 'values'
        if key == option:
            return json.dumps(self.choices)
        return ttk.Combobox.cget(self, key)
    
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
        if type(values) == type(''):
            obj = None
            # try json string
            try:
                obj = json.loads(values)
            except ValueError:
                obj = values
            if type(obj) == type([]):
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
            if type(v) != type('') and len(v) == 2:
                key, value = v
            self._choices[key] = value
    
    def current(self, key=None):
        idx = ttk.Combobox.current(self, None)
        index = -1
        ckey = None
        for i, k in enumerate(self._choices.keys()):
            if key is None and idx == i:
                ckey = k
                break
            elif key == k:
                index = i
                break
        if key is None:
            return ckey
        return ttk.Combobox.current(self, index)
    
    def set(self, key):
        value = self._choices[key]
        return ttk.Combobox.set(self, value)


if __name__ == '__main__':
    def show_selection(event):
        cbox = event.widget
        print('values:', cbox.cget('values'))
        print('current:', cbox.current())
    
    root = tk.Tk()
    c = Combobox(root, values='[["DNI", "Doc.Nac.Id."], ["LE", "Libreta Enrolamiento"]]')
    c.bind('<<ComboboxSelected>>', show_selection)
    c.set('LE')
    c.grid()
    
    values = (('tres', 3), (4, 'cuatro'), (6, "seis"))
    c = Combobox(root, values=values)
    c.bind('<<ComboboxSelected>>', show_selection)
    c.set(6)
    c.grid()
    
    values = (('A', 'A label'), ('B', 'B label'), ('C', "C label"))
    c = Combobox(root)
    c.bind('<<ComboboxSelected>>', show_selection)
    c.configure(values=values)
    c.set('B')
    c.grid()
    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
