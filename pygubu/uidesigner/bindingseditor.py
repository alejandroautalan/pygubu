from __future__ import unicode_literals
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

class BindingsEditor:
    def __init__(self, etreeview):
        self.tv = etreeview
        self._curr_data = None
        self._adder = 'adder'
        self._allow_edit = False
        self.tv.insert('', tk.END, iid=self._adder, values=('+',))
        self.tv.bind('<<TreeviewInplaceEdit>>', self._on_inplace_edit)
        self.tv.bind('<<TreeviewCellEdited>>', self._on_cell_edited)
        self.tv.bind('<Double-Button-1>', self._on_add_clicked, add=True)

        self._del_btn = ttk.Button(self.tv, text='-',
            command=self._on_del_clicked)

    def _on_add_clicked(self, event):
        sel =  self.tv.selection()
        if sel:
            item = sel[0]
            if item == self._adder and self._allow_edit:
                self._add_binding(('<1>', 'callback', ''))

    def _on_del_clicked(self):
        sel =  self.tv.selection()
        if sel:
            item = sel[0]
            self.tv.delete(item)
        self._copy_to_data()

    def _on_cell_edited(self, event):
        col, item = self.tv.get_event_info()
        self._copy_to_data()

    def _copy_to_data(self):
        if self._curr_data is not None:
            items = self.tv.get_children()
            self._curr_data.clear_bindings()
            for item in items:
                if item != self._adder:
                    values = self.tv.item(item, 'values')
#                    print(item, 'values = ', values)
                    self._curr_data.add_binding(*values[:3])
                    self._curr_data.notify(self)

    def _add_binding(self, bind):
        idx = self.tv.index(self._adder)
        item = self.tv.insert('', idx, values=bind)
        self.tv.selection_set('')

    def edit(self, data):
        self.clear()
        self._curr_data = data
        for bind in data.get_bindings():
            self._add_binding(bind)

    def allow_edit(self, var):
        self._allow_edit = var


    def _on_inplace_edit(self, event):
        col, item = self.tv.get_event_info()
#        print('on_inplace_edit:', col, item)
        if item != self._adder and self._allow_edit:
            if col in ('sequence', 'handler'):
                self.tv.inplace_entry(col, item)
            elif col in ('add',):
                self.tv.inplace_checkbutton(col, item, offvalue='')
            elif col in ('actions',):
                self.tv.inplace_custom(col, item, self._del_btn)


    def clear(self):
        children = self.tv.get_children()
        for item in children:
            if item != self._adder:
                self.tv.delete(item)
