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

import tkinter
import tkinter.ttk as ttk

class DialogBase():
    def __init__(self, parent, **kw):
        self.parent = parent
        self.running_modal = True
        self.master = tkinter.Toplevel(parent)

        self.body_frame = body = ttk.Frame(self.master)
        self.initial_focus = self._create_body(body)
        if not self.initial_focus:
            self.initial_focus = body
        body.pack(fill='both', expand=True)
        self.btnbox_frame = f = ttk.Frame(self.master)
        self._create_btnbox(f)
        f.pack(fill='x')

        if not self.initial_focus:
            self.initial_focus = self


    def _create_body(self, parent):
        #implement me on sublcass
        return parent


    def run(self):
        self.rundialog(False)


    def run_modal(self):
        self.rundialog(True)


    def rundialog(self, modal=True):
        self.running_modal = modal
        self.master.transient(self.parent)
        self.master.wait_visibility()
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.initial_focus.focus_set()
        if modal:
            self.master.grab_set()
            self.master.wait_window(self.master)


    def close(self):
        self.parent.focus_set()
        if self.running_modal:
            self.master.destroy()
        else:
            self.master.withdraw()


    def show(self):
        if not self.running_modal:
            self.master.deiconify()


    def set_title(self, title):
        """Sets the dialog title"""
        if self.master:
            self.master.title(title)


    def _create_btnbox(self, parent):
        self.cancel_btn = o = ttk.Button(parent, text='Cancel',
            command=self.close)
        o.pack(side='right')
        self.ok_btn = o = ttk.Button(parent, text='Ok',
            command=self.on_ok_execute)
        o.pack(side='right')
        o.bind("<Return>", self.on_ok_execute)


    def on_ok_execute(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.master.withdraw()
        self.master.update_idletasks()

        try:
            self.apply()
        finally:
            self.close()


    def validate(self):
        return True


    def apply(self):
        pass


if __name__ == '__main__':
    class TestDialog(DialogBase):
        def _create_body(self, master):
            label = ttk.Label(master, text='TestDialog Class')
            label.pack()
            return label

    app = tkinter.Tk()
    dialog = None

    def show_dialog():
        global dialog
        if dialog is None:
            dialog = TestDialog(app)
            dialog.run()
        else:
            dialog.show()

    def show_modal_dialog():
        dialog = TestDialog(app)
        dialog.set_title('Modal dialog')
        dialog.run_modal()

    btn = tkinter.Button(app, text='show dialog', command=show_dialog)
    btn.pack()
    btn = tkinter.Button(app, text='show modal dialog', command=show_modal_dialog)
    btn.pack()

    app.mainloop()

