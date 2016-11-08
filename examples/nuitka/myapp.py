#file: myapp.py
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import pygubu

#Help nuitka compiler to include specific modules
import nuitkahelper


class MyApplication:

    def __init__(self):
        self.builder = b = pygubu.Builder()
        b.add_from_file('myapp.ui')
        self.mainwindow = b.get_object('mainwindow')
        b.connect_callbacks(self)

    def on_action1_clicked(self):
        tk.messagebox.showinfo('Myapp', 'Action 1 clicked')

    def on_action2_clicked(self):
        tk.messagebox.showinfo('Myapp', 'Action 2 clicked')

    def on_action3_clicked(self):
        tk.messagebox.showinfo('Myapp', 'Action 3 clicked')

    def on_appmenu_action(self, command_id):
        tk.messagebox.showinfo('Myapp', 'Byby!')
        self.mainwindow.quit()
    
    def run(self):
        self.mainwindow.mainloop();


if __name__ == '__main__':
    app = MyApplication()
    app.run();
