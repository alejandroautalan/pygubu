import sys
import tkinter
from tkinter import ttk
import myttk
import tkbuilder


class UITester(myttk.Application):
    def _create_ui(self):
        self.builder = tkbuilder.Tkbuilder()
        self.builder.add_from_file(sys.argv[1])
        self.builder.get_object(self, 'mainwindow')

        self.grid(row=0, column=0, sticky='nswe')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.set_resizable()

try:
    __file__
except:
    sys.argv = [sys.argv[0], 'exampleui_2.tkb']

if __name__ == '__main__':
    app = UITester(tkinter.Tk())
    app.run()
