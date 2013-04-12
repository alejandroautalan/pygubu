import sys
import os

import tkinter
from tkinter import messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

import pygubu


class Myapp:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        fpath = os.path.join(os.path.dirname(__file__),"button_cb.ui")
        builder.add_from_file(fpath)

        mainwindow = builder.get_object('mainwindow', master)

        builder.connect_commands(self)

        callbacks = {
            'on_button2_clicked': self.on_button2_clicked
            }

        builder.connect_commands(callbacks)

    def on_my_button_clicked(self):
        messagebox.showinfo('From callback', 'My button was clicked !!')

    def on_button2_clicked(self):
        messagebox.showinfo('From callback', 'Button 2 was clicked !!')

if __name__ == '__main__':
    tk = tkinter.Tk()
    app = Myapp(tk)
    tk.mainloop()

