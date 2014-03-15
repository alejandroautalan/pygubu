# encoding: UTF-8
#
# Copyright 2012-2013 Alejandro Autalán
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  http://pygubu.web.here

from __future__ import unicode_literals
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


class Dialog(object):
    """
    Virtual events:
        <<DialogClose>>
    """

    def __init__(self, parent, modal=False):
        self.parent = parent
        self.is_modal = modal
        self.running_modal = False
        self.toplevel = tk.Toplevel(parent)
        self.toplevel.withdraw()
        self.toplevel.protocol("WM_DELETE_WINDOW", self._on_wm_delete_window)
        self.bind('<<DialogClose>>', self._default_close_action)

        self._init_before()
        self._create_ui()
        self._init_after()

        #self.frame.pack(fill='both', expand=True)


    def _init_before(self):
        pass

    def _create_ui(self):
        pass

    def _init_after(self):
        pass


    def set_modal(self, modal):
        self.is_modal = modal
        
    
    def run(self):
        self.toplevel.transient(self.parent)
        self.toplevel.deiconify()
        self.toplevel.wait_visibility()
        initial_focus = self.toplevel.focus_lastfor()
        if initial_focus:
            initial_focus.focus_set()
        if self.is_modal:
            self.running_modal =True
            self.toplevel.grab_set()
            

    def destroy(self):
        if self.toplevel:
            self.toplevel.destroy()
        self.toplevel = None


    def _on_wm_delete_window(self):
        self.toplevel.event_generate('<<DialogClose>>')
        
    
    def _default_close_action(self, dialog):
        self.close()


    def close(self):
        if self.running_modal:
            self.toplevel.grab_release()
            self.running_modal = False
        self.toplevel.withdraw()
        self.parent.focus_set()


    def show(self):
        if self.toplevel:
            self.toplevel.deiconify()


    def set_title(self, title):
        """Sets the dialog title"""
        if self.toplevel:
            self.toplevel.title(title)

    #
    # interface to toplevel methods used by gui builder
    #
    def configure(self, cnf=None, **kw):
        self.toplevel.configure(cnf, **kw)
    
    config = configure

    def cget(self, key):
        return self.toplevel.cget(key)

    __getitem__ = cget

    def __setitem__(self, key, value):
        self.configure({key: value})

    def bind(self, sequence=None, func=None, add=None):
        def dialog_cb(event, dialog=self):
            func(dialog)
        return self.toplevel.bind(sequence, dialog_cb, add)
        
#    def unbind(self, sequence, funcid=None):
#        pass


if __name__ == '__main__':
    class TestDialog(Dialog):
        def _create_ui(self):
            label = ttk.Label(self.frame, text='TestDialog Class')
            label.pack()
            entry = ttk.Entry(self.frame)
            entry.pack()
#            f = ttk.Frame(self.toplevel)
#            self.default_buttonbox(f)
#            f.pack(fill='x')

    app = tk.Tk()
    dialog = None

    def show_dialog():
        global dialog
        if dialog is None:
            dialog = TestDialog(app)
            dialog.run()
        else:
            dialog.show()
            
    def custom_callback(dialog):
        print('Custom callback')
        dialog.close()

    def show_modal_dialog():
        dialog = TestDialog(app)
        dialog.set_title('Modal dialog')
        dialog.set_modal(True)
        dialog.bind('<<DialogClose>>', custom_callback)
        print('before run')
        dialog.run()
        print('after run')

    btn = tk.Button(app, text='show dialog', command=show_dialog)
    btn.pack()
    btn = tk.Button(app, text='show modal dialog', command=show_modal_dialog)
    btn.pack()

    app.mainloop()
