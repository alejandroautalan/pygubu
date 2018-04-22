# encoding: utf8
# menu.py
try:
    import tkinter as tk
    from tkinter import messagebox
except:
    import Tkinter as tk
    import tkMessageBox as messagebox
import pygubu

class MyApplication(pygubu.TkApplication):

    def _create_ui(self):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('menu.ui')

        #3: Create the widget using self.master as parent
        self.mainwindow = builder.get_object('mainwindow', self.master)

        # Set main menu
        self.mainmenu = menu = builder.get_object('mainmenu', self.master)
        self.set_menu(menu)

        # Configure callbacks
        builder.connect_callbacks(self)


    def on_mfile_item_clicked(self, itemid):
        if itemid == 'mfile_open':
            messagebox.showinfo('File', 'You clicked Open menuitem')

        if itemid == 'mfile_quit':
            messagebox.showinfo('File', 'You clicked Quit menuitem. Byby')
            self.quit();


    def on_about_clicked(self):
        messagebox.showinfo('About', 'You clicked About menuitem')


if __name__ == '__main__':
    root = tk.Tk()
    app = MyApplication(root)
    app.run()
