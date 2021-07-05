# encoding: utf8
from __future__ import print_function
from collections import OrderedDict
import json
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


class Combobox(ttk.Combobox, object):
    """
    A ttk.Combobox that accepts a list of (key, label) pair of options.
    """
    def __init__(self, master=None, **kw):
        self._keyvarcb = None
        self._txtvarcb = None
        self._choices = OrderedDict()
        
        self.__options = options = {
            'keyvariable': None,
            'textvariable': None,
        }
        # remove custom options from kw before initialization
        for k, v in options.items():
            options[k] = kw.pop(k, v)
        
        key = 'values'
        if key in kw:
            values = kw[key]
            self.choices = values
            values = self.__choices2tkvalues(self.choices)
            kw[key] = values
        
        # only normal/disabled supported
        # normal is converted to readonly
        key = 'state'
        if key in kw:
            if kw[key] not in ('readonly', 'disabled'):
                kw[key] = 'readonly'
        else:
            kw[key] = 'readonly'
            
        ttk.Combobox.__init__(self, master, **kw)
        
        self.__config_keyvar(options['keyvariable'])
        self.configure(textvariable=options['textvariable'])
    
    def __config_keyvar(self, var):
        if var is None:
            return
        
        def on_keyvar_changed(varname, elementname, mode):
            nvalue = self.__options['keyvariable'].get()
            if nvalue in self._choices:
                self.current(nvalue)
        
        keyvar = self.__options['keyvariable']
        if self._keyvarcb is not None:
            keyvar.trace_vdelete('w', self._keyvarcb)
        self.__options['keyvariable'] = var
        self._keyvarcb = var.trace(mode="w", callback=on_keyvar_changed)
        
        # A textvariable is needed if keyvariable is set
        txtvar = self.cget('textvariable')
        if not txtvar:
            var = tk.StringVar()
            self.configure(textvariable=var)
        else:
            self.__config_txtvar(txtvar)
        
    def __config_txtvar(self, var):
        keyvar = self.__options['keyvariable']
        if var is None or keyvar is None:
            return
        
        def on_txtvar_changed(varname, elementname, mode):
            ckey = self.current()
            keyvar.set(ckey)
        
        txtvar = self.cget('textvariable')
        if txtvar and self._txtvarcb is not None:
            txtvar.trace_vdelete('w', self._txtvarcb)
        self.__options['textvariable'] = var
        self._txtvarcb = var.trace(mode="w", callback=on_txtvar_changed)
            
    def configure(self, cnf=None, **kw):
        args = tk._cnfmerge((cnf, kw))
        key = 'values'
        if key in args:
            self.choices = args[key]
            args[key] = self.__choices2tkvalues(self.choices)
            # clear variables:
            keyvar = self.__options['keyvariable']
            if keyvar is not None:
                keyvar.set('')
            txtvar = self.cget('textvariable')
            if txtvar is not None:
                txtvar.set('')
        key = 'keyvariable'
        if key in args:
            value = args.pop(key)
            self.__config_keyvar(value)
            return
        key = 'textvariable'
        if key in args:
            value = args[key]
            self.__config_txtvar(value)
        
        # only readonly and disabled supported
        key = 'state'
        if key in args:
            if args[key] not in ('readonly', 'disabled'):
                args[key] = 'readonly'
        return ttk.Combobox.configure(self, args)

    config = configure

    def cget(self, key):
        option = 'values'
        if key == option:
            return json.dumps(self.choices)
        option = 'keyvariable'
        if key == option:
            return self.__options[key]
        option = 'textvariable'
        if key == option:
            return self.__options[key]
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
            if type(v) != type(u'') and len(v) == 2:
                key, value = v
            self._choices[key] = value
    
    def current(self, key=None):
        idx = ttk.Combobox.current(self, None)
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
        return ttk.Combobox.current(self, index)
    
    def set(self, key):
        value = self._choices[key]
        return ttk.Combobox.set(self, value)
        
    def get(self):
        return self.current()


if __name__ == '__main__':
    def show_selection(event):
        cbox = event.widget
        print('values:', cbox.cget('values'))
        print('current:', cbox.current())
    
    root = tk.Tk()
    txtvalues = '[["DNI", "Doc.Nac.Id."], ["LE", "Libreta Enrolamientox"]]'
    c = Combobox(root, values=txtvalues)
    c.bind('<<ComboboxSelected>>', show_selection)
    c.configure(values=txtvalues)
    c.set('LE')
    c.grid()
    
    values = (('tres', 3), (4, 'cuatro'), (6, "seis"))
    c = Combobox(root, values=values)
    c.bind('<<ComboboxSelected>>', show_selection)
    c.set(6)
    c.grid()
    
    var = tk.StringVar()
    var.set('C')
    e = ttk.Entry(root, textvariable=var)
    e.grid()
    
    var2 = tk.StringVar()
    var2.set('A')
    e2 = ttk.Entry(root, textvariable=var2)
    e2.grid()
    
    values = (('', 'Seleccione Opción'),
              ('A', 'A label'),
              ('B', 'B label'),
              ('C', "C label"))
    c = Combobox(root, textvariable=var)
    c.bind('<<ComboboxSelected>>', show_selection)
    c.configure(values=values)
    c.set('')
    c.grid()
    
    c.configure(keyvariable=var2)
    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
