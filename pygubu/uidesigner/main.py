# This file is part of pygubu.

#
# Copyright 2012 Alejandro Autalán
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

import os
import xml.dom.minidom
import xml.etree.ElementTree as ET

import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import pygubu
from pygubu import builder
from . import util
from . import properties
from .propertieseditor import WidgetPropertiesEditor
from .widgeteditor import WidgetsTreeEditor


#Initilize properties from custom widgets
for pname, descr in builder.CUSTOM_PROPERTIES.items():
    properties.register_custom(pname, descr)


class PreviewHelper:
    def __init__(self, notebook):
        self.notebook = notebook
        self.builders = {}
        self.canvases = {}
        self.tabs = {}
        self.windows = {}
        self.preview_tag = 'previewwindow'

    def draw(self, identifier, widget_id, xmlnode, is_menu=False):
        uibuilder = pygubu.Builder()
        canvas = None
        if identifier not in self.builders:
            canvas = util.create_scrollable(self.notebook, tkinter.Canvas,
                background='white', scrollregion="0 0 80i 80i")
            canvas.create_window(5, 5, anchor=tkinter.NW,
                tags=self.preview_tag)
            self.canvases[identifier] = canvas
            self.notebook.add(canvas.frame, text=widget_id,
                sticky=tkinter.NSEW)
            self.tabs[identifier] = canvas.frame
        else:
            self.notebook.tab(self.tabs[identifier], text=widget_id)
            del self.builders[identifier]
            canvas = self.canvases[identifier]
            canvas.itemconfigure(self.preview_tag, window='')
            window = self.windows[identifier]
            window.destroy()

        uibuilder.add_from_xmlnode(xmlnode)
        self.builders[identifier] = uibuilder

        preview_widget = None
        if is_menu:
            menubutton = ttk.Menubutton(canvas, text='Menu preview')
            widget = uibuilder.get_object(widget_id, menubutton)
            menubutton.configure(menu=widget)
            preview_widget = menubutton
        else:
            preview_widget = uibuilder.get_object(widget_id, canvas)

        self.windows[identifier] = preview_widget
        canvas.itemconfigure(self.preview_tag, window=preview_widget)


    def delete(self, identifier):
        self.notebook.forget(self.tabs[identifier])
        del self.tabs[identifier]
        self.windows[identifier].destroy()
        del self.windows[identifier]



class PygubuUI(util.Application):
    """Main gui class"""

    def _create_ui(self):
        """Creates all gui widgets"""

        self.preview = None
        self.builder = builder = pygubu.Builder()
        self.currentfile = None
        self.is_changed = False

        print(os.path.dirname(os.path.abspath(__file__)))
        uifile = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),"ui/pygubu-ui.ui")
        builder.add_from_file(uifile)

        #build main ui
        builder.get_object('mainwindow', self)
        toplevel = self.winfo_toplevel()
        menu = builder.get_object('mainmenu', toplevel)
        toplevel['menu'] = menu

        #project name
        self.project_name = self.builder.get_object('projectname_lbl')

        #Class selector values
        self.widgetlist = self.builder.get_object("widgetlist")
        self.configure_widget_list()

        #widget tree
        self.treeview = tree = builder.get_object('treeview1')

        #Preview
        nbpreview = builder.get_object('notebookpreview')
        self.previewer = PreviewHelper(nbpreview)
        #tree editor
        self.tree_editor = WidgetsTreeEditor(self)
        #properties frame
        self.widget_props_frame = builder.get_object('propertiesframe')
        self.layout_props_frame = builder.get_object('layoutframe')
        self.properties_editor = WidgetPropertiesEditor(self)

        self.builder.connect_commands(self)

        self.grid(row=0, column=0, sticky='nswe')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.set_resizable()

        #app config
        self.set_title('Pygubu a GUI builder for tkinter')
        self.set_size('800x600')


    def configure_widget_list(self):
        tv = self.widgetlist
        tv.heading('#0', text='Widget List')
        tv.bind('<Double-1>', lambda e: self.on_add_widget_event())
        values = list(builder.CLASS_MAP.keys())
        values.sort()
        for value in values:
            tv.insert('', tkinter.END, text=value)


    def on_add_widget_event(self):
        wlist = self.widgetlist
        #get widget class name to insert
        selection = wlist.selection()
        if selection:
            item = selection[0]
            wclass = wlist.item(item, 'text')
            self.tree_editor.add_widget(wclass)


    def on_menuitem_new_clicked(self):
        new = True
        if self.is_changed:
            new = openfile = messagebox.askokcancel('File changed',
                'Changes not saved. Discard Changes?')
        if new:
            self.tree_editor.remove_all()
            self.is_changed = False
            self.project_name.configure(text='<None>')


    def on_menuitem_open_clicked(self):
        """Opens xml file and load to treeview"""
        openfile = True
        if self.is_changed:
            openfile = messagebox.askokcancel('File changed',
                'Changes not saved. Open new file anyway?')
        if openfile:
            fname = filedialog.askopenfilename()
            if fname:
                self.load_file(fname)
                self.currentfile = fname
                self.is_changed = False


    def on_menuitem_save_clicked(self):
        """Save treeview to xml file"""

        if self.currentfile:
            if self.is_changed:
                self.do_save(self.currentfile)
        else:
            self.do_save_as()


    def on_menuitem_saveas_clicked(self):
        self.do_save_as()


    def on_menuitem_quit_clicked(self):
        self.quit()


    def on_close_execute(self):
        quit = True
        if self.is_changed:
            quit = messagebox.askokcancel('File changed',
                'Changes not saved. Quit anyway?')
        return quit


    def do_save(self, fname):
        self.save_file(fname)
        self.currentfile = fname
        self.is_changed = False


    def do_save_as(self):
        fname = filedialog.asksaveasfilename()
        if fname:
            self.do_save(fname)


    def save_file(self, filename):
        self.project_name.configure(text=filename)
        xml_tree = self.tree_editor.tree_to_xml()
        xmlvar = xml.dom.minidom.parseString(
            ET.tostring(xml_tree.getroot()))
        pretty_xml_as_string = xmlvar.toprettyxml(indent=' '*4)
        with open(filename, 'w') as f:
            f.write(pretty_xml_as_string)


    def set_changed(self):
        self.is_changed = True


    def load_file(self, filename):
        """Load xml into treeview"""

        self.tree_editor.load_file(filename)
        self.project_name.configure(text=filename)


def start_pygubu():
    app = PygubuUI(tkinter.Tk())
    app.run()


if __name__ == '__main__':
    start_pygubu()

