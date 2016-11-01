# encoding: utf8
from __future__ import unicode_literals
import sys
import os

try:
    import tkinter as tk
    from tkinter import messagebox
except:
    import Tkinter as tk
    import tkMessageBox as messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

import pygubu


class Myapp:
    def __init__(self, master):
        self.master = master
        self.builder = builder = pygubu.Builder()
        fpath = os.path.join(os.path.dirname(__file__),"commands.ui")
        builder.add_from_file(fpath)

        mainwindow = builder.get_object('mainwindow', master)

        builder.connect_callbacks(self)
        self.set_scrollbars()

    def on_button_clicked(self):
        messagebox.showinfo('From callback', 'Button clicked !!')

    def validate_number(self, P):
        print('On validate number')
        value = unicode(P)
        return value == '' or value.isnumeric()

    def entry_invalid(self):
        messagebox.showinfo('Title', 'Invalid entry input')

    def radiobutton_command(self):
        messagebox.showinfo('Title', 'Radiobutton command')

    def checkbutton_command(self):
        messagebox.showinfo('Title', 'Checkbutton command')

    def on_scale1_changed(self, event):
        label = self.builder.get_object('scale1label')
        scale = self.builder.get_object('scale1')
        label.configure(text=scale.get())

    def on_scale2_changed(self, event):
        label = self.builder.get_object('scale2label')
        scale = self.builder.get_object('scale2')
        label.configure(text=int(scale.get()))

    def set_scrollbars(self):
        sb1 = self.builder.get_object('scrollbar_1')
        sb2 = self.builder.get_object('scrollbar_2')
        sb1.set(.0, .20)
        sb2.set(.0, .20)

    def on_scrollbar1_changed(self, *args):
        label = self.builder.get_object('scrollbar1label')
        label.configure(text=repr(args))

    def on_scrollbar2_changed(self, *args):
        label = self.builder.get_object('scrollbar2label')
        label.configure(text=repr(args))

    def on_spinbox_cmd(self):
        def showmessage():
            messagebox.showinfo('Title', 'Spinbox command')
        self.master.after_idle(showmessage)

    def on_combobox_validate(self, P):
        value = unicode(P)
        return value == '' or value.isnumeric()

    def on_combobox_invalid(self, P):
        messagebox.showinfo('Title', 'Invalid combobox input')

    def on_combobox_postcmd(self):
        messagebox.showinfo('Title', 'Combobox postcommand')

    def on_menuitem_clicked(self, itemid):
        messagebox.showinfo('Title',
            'Menu item "{0}" was clicked'.format(itemid))

    def on_menuitem2_clicked(self):
        messagebox.showinfo('Title', 'Callback on_menuitem2_clicked')

if __name__ == '__main__':
    root = tk.Tk()
    app = Myapp(root)
    root.mainloop()

