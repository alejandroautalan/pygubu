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

import logging
import xml.etree.ElementTree as ET
import tkinter
from tkinter import ttk


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('pygubu.builder')


CLASS_MAP = {}

def register(classname, classobj):
    CLASS_MAP[classname] = classobj

CUSTOM_PROPERTIES = {}

def register_property(name, description):
    CUSTOM_PROPERTIES[name] = description


#
# Base class
#
class BuilderObject:
    @classmethod
    def factory(cls, master, properties=None, layout_properties=None):
        clsobj = cls(master, properties, layout_properties)
        return clsobj

    def __init__(self, master, properties=None, layout_prop=None):
        self.widget = self.class_(master)
        self.properties = properties
        self.layout_properties = layout_prop

    def configure(self):
        for pname, value in self.properties.items():
            self.widget[pname] = value

    def layout(self):
        #use grid layout for all
        properties = self.layout_properties
        grid_rows = properties.pop('grid_rows', {})
        grid_cols = properties.pop('grid_columns', {})

        self.widget.grid(**properties)

        #get grid row and col properties:
        for row in grid_rows:
            self.widget.rowconfigure(row, **grid_rows[row])
        for col in grid_cols:
            self.widget.columnconfigure(col, **grid_cols[col])

    def get_child_master(self):
        return self.widget

    def add_child(self, cwidget):
        pass


#
# tkinter widgets
#
class TKFrame(BuilderObject):
    class_ = tkinter.Frame
    container = True
    properties = ['background', 'borderwidth', 'cursor', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'padx', 'pady', 'relief', 'takefocus', 'width']

register('tk.Frame', TKFrame)


class TKLabel(BuilderObject):
    class_ = tkinter.Label
    container = False
    properties = ['activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'compound',
        'cursor', 'disabledforeground', 'font', 'foreground', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'justify', 'padx', 'pady', 'relief', 'state',
        'takefocus', 'text', 'textvariable', 'underline',
        'width', 'wraplength']

register('tk.Label', TKLabel)


class TKLabelFrame(BuilderObject):
    class_ = tkinter.LabelFrame
    container = True
    properties = ['background', 'borderwidth', 'cursor', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'labelanchor', 'labelwidget', 'padx', 'pady', 'relief',
        'takefocus', 'width']
#TODO: Add helper so the labelwidget can be configured on GUI

register('tk.LabelFrame', TKLabelFrame)


class TKEntry(BuilderObject):
    class_ = tkinter.Entry
    container = False
    properties = ['background', 'borderwidth', 'cursor',
        'disabledbackground', 'disabledforeground', 'exportselection',
        'foreground', 'font', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'insertbackground', 'insertborderwidth',
        'insertofftime', 'insertontime', 'insertwidth', 'justify',
        'readonlybackground', 'relief', 'selectbackground',
        'selectborderwidth', 'selectforeground', 'show', 'state',
        'takefocus', 'textvariable', 'validate', 'validatecommand',
        'width', 'wraplength', 'xscrollcommand']

register('tk.Entry', TKEntry)


class TKButton(BuilderObject):
    class_ = tkinter.Button
    container = False
    properties = ['activebackground', 'activeforeground', 'anchor',
        'borderwidth', 'background', 'bitmap', 'command', 'cursor',
        'default', 'disabledforeground', 'foreground', 'font', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'justify', 'overrelief', 'padx', 'pady', 'relief',
        'repeatdelay', 'repeatinterval', 'state', 'takefocus', 'text',
        'textvariable', 'underline', 'width', 'wraplength']

register('tk.Button', TKButton)


class TKCheckbutton(BuilderObject):
    class_ = tkinter.Checkbutton
    container = False
    properties = ['activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'command', 'compound',
        'cursor', 'disabledforeground', 'font', 'foreground', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'indicatoron', 'justify', 'offrelief', 'offvalue',
        'onvalue', 'overrelief', 'padx', 'pady', 'relief', 'selectcolor',
        'selectimage', 'state', 'takefocus', 'text', 'textvariable',
        'underline', 'variable', 'width', 'wraplength']

register('tk.Checkbutton', TKCheckbutton)


class TKListbox(BuilderObject):
    class_ =  tkinter.Listbox
    container = False
    properties = ['activestyle', 'background', 'borderwidth', 'cursor',
            'disabledforeground', 'exportselection', 'font',
            'foreground', 'height', 'highlightbackground', 'highlightcolor',
            'highlightthickness', 'listvariable', 'relief',
            'selectbackground', 'selectborderwidth', 'selectforeground',
            'selectmode', 'state', 'takefocus', 'width', 'xscrollcommand',
            'yscrollcommand']

register('tk.Listbox', TKListbox)


class TKText(BuilderObject):
    class_ = tkinter.Text
    container = False
    properties = ['autoseparators', 'background', 'borderwidth', 'cursor',
            'exportselection', 'font',
            'foreground', 'height', 'highlightbackground', 'highlightcolor',
            'highlightthickness', 'insertbackground', 'insertborderwidth',
            'insertofftime', 'insertontime', 'insertwidth',
            'maxundo', 'padx', 'pady', 'relief', 'selectbackground',
            'selectborderwidth', 'selectforeground', 'spacing1',
            'spacing2', 'spacing3', 'state', 'tabs', 'takefocus',
            'undo', 'width', 'wrap', 'xscrollcommand', 'yscrollcommand',
            ]

register('tk.Text', TKText)


class PanedWindow(BuilderObject):
    class_ = None
    container = True
    properties = []

    def __init__(self, master, properties, layout_prop):
        orient = properties.pop('orient', 'vertical')
        self.widget = self.class_(master, orient=orient)
        self.properties = properties
        self.layout_properties = layout_prop


class PanedWindowPane(BuilderObject):
    class_ = None
    container = True
    properties = []

    def __init__(self, master, properties, layout_prop):
        self.widget = master
        self.properties= properties
        self.layout_properties = layout_prop

    def configure(self):
        pass

    def layout(self):
        pass

    def add_child(self, cwidget):
        self.widget.add(cwidget, **self.properties)


class TKPanedWindow(PanedWindow):
    class_ = tkinter.PanedWindow
    properties = ['background', 'borderwidth', 'cursor', 'handlepad',
        'handlesize', 'height', 'opaqueresize', 'orient', 'relief',
        'sashpad', 'sashrelief', 'sashwidth', 'showhandle', 'width']

register('tk.PanedWindow', TKPanedWindow)


class TKPanedWindowPane(PanedWindowPane):
    class_ = None
    container = True
    properties = ['height', 'minsize', 'padx', 'pady', 'sticky']

register('tk.PanedWindow.Pane', TKPanedWindowPane)


class TKMenubutton(BuilderObject):
    class_ = tkinter.Menubutton
    container = True
    properties = ['activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'compound', 'cursor',
        'direction', 'disabledforeground', 'foreground', 'font',
        'height', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'image', 'justify', 'padx',
        'pady', 'relief', 'state', 'takefocus', 'text', 'textvariable',
        'underline', 'width', 'wraplength']

    def add_child(self, cwidget):
        self.widget['menu'] = cwidget

register('tk.Menubutton', TKMenubutton)


class TKMessage(BuilderObject):
    class_ = tkinter.Message
    container = False
    properties = ['aspect', 'background', 'borderwidth', 'cursor',
        'font', 'foreground', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'justify', 'padx', 'pady', 'relief',
        'takefocus', 'text', 'textvariable', 'width']

register('tk.Message', TKMessage)


class TKRadiobutton(BuilderObject):
    class_ = tkinter.Radiobutton
    container = False
    properties = ['activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'command', 'compound',
        'cursor', 'disabledforeground', 'font', 'foreground', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'indicatoron', 'justify', 'offrelief', 'overrelief',
        'padx', 'pady', 'relief', 'selectcolor', 'selectimage', 'state',
        'takefocus', 'text', 'textvariable',
        'underline', 'variable', 'width', 'wraplength']

register('tk.Radiobutton', TKRadiobutton)


class TKScale(BuilderObject):
    class_ = tkinter.Scale
    container = False
    properties = ['activebackground', 'background', 'borderwidth', 'command',
        'cursor', 'digits', 'font', 'foreground', 'from_',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'label', 'length', 'orient', 'relief', 'repeatdelay', 'repeatinterval',
        'resolution', 'showvalue', 'sliderlenght', 'sliderrelief', 'state',
        'takefocus', 'tickinterval', 'to', 'troughcolor', 'variable', 'width']

register('tk.Scale', TKScale)


class TKScrollbar(BuilderObject):
    class_ = tkinter.Scrollbar
    container = False
    properties = ['activebackground', 'activerelief', 'background',
        'borderwidth', 'command', 'cursor', 'elementborderwidth',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'jump', 'orient', 'relief', 'repeatdelay', 'repeatinterval',
        'takefocus', 'troughcolor', 'width']

register('tk.Scrollbar', TKScrollbar)


class TKSpinbox(BuilderObject):
    class_ = tkinter.Entry
    container = False
    properties = ['activebackground', 'background', 'borderwidth',
        'buttonbackground', 'buttoncursor', 'buttondownrelief', 'buttonup',
        'command', 'cursor', 'disabledbackground', 'disabledforeground',
        'exportselection', 'font', 'foreground', 'format', 'from_',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'increment', 'insertbackground', 'insertborderwidth',
        'insertofftime', 'insertontime', 'insertwidth', 'justify',
        'readonlybackground', 'relief', 'repeatdelay', 'repeatinterval',
        'selectbackground', 'selectborderwidth', 'selectforeground', 'state',
        'takefocus', 'textvariable', 'to', 'values', 'width', 'wrap',
        'xscrollcommand']

register('tk.Spinbox', TKSpinbox)


#
# ttk widgets
#

class TTKFrame(BuilderObject):
    class_ = ttk.Frame
    container = True
    properties = ['class_', 'cursor', 'height', 'padding',
            'relief', 'style', 'takefocus', 'width']

register('ttk.Frame', TTKFrame)


class TTKLabel(BuilderObject):
    class_ = ttk.Label
    container = False
    properties = ['anchor', 'background', 'borderwidth',
            'class_', 'compound', 'cursor', 'font', 'foreground',
            'image', 'justify', 'padding', 'relief',
            'style', 'takefocus', 'text', 'textvariable', 'underline',
            'width', 'wraplength']

register('ttk.Label', TTKLabel)


class TTKButton(BuilderObject):
    class_= ttk.Button
    container= False
    properties = ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline']

register('ttk.Button', TTKButton)


class TTKCheckbutton(BuilderObject):
    class_ = ttk.Checkbutton
    container = False
    properties = ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'variable', 'offvalue', 'onvalue', 'width']

register('ttk.Checkbutton', TTKCheckbutton)


class TTKRadiobutton(BuilderObject):
    class_ = ttk.Radiobutton
    container = False
    properties = ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'value', 'variable', 'width']

register('ttk.Radiobutton', TTKRadiobutton)


class TTKCombobox(BuilderObject):
    class_ = ttk.Combobox
    container = False
    properties = ['class_', 'cursor', 'exportselection',
            'height', 'justify', 'postcommand', 'style', 'takefocus',
            'textvariable', 'validate', 'validatecommand', 'values',
            'width', 'xscrollcommand', 'state']

register('ttk.Combobox', TTKCombobox)


class TTKScrollbar(BuilderObject):
    class_ = ttk.Scrollbar
    container = False
    properties = ['class_', 'command', 'cursor', 'orient',
        'style', 'takefocus']

register('ttk.Scrollbar', TTKScrollbar)


class TTKSizegrip(BuilderObject):
    class_ = ttk.Sizegrip
    container = False
    properties = ['class_', 'style']

register('ttk.Sizegrip', TTKSizegrip)


class TTKEntry(BuilderObject):
    class_ = ttk.Entry
    container = False
    properties = ['class_', 'cursor', 'exportselection', 'font',
            'invalidcommand', 'justify', 'show', 'style', 'takefocus',
            'textvariable', 'validate', 'validatecommand', 'values',
            'width', 'xscrollcommand']

register('ttk.Entry', TTKEntry)


class TTKProgressbar(BuilderObject):
    class_ = ttk.Progressbar
    container = False
    properties = ['class_', 'cursor', 'length', 'maximum', 'mode',
            'orient', 'style', 'takefocus', 'variable']

register('ttk.Progressbar', TTKProgressbar)


class TTKScale(BuilderObject):
    class_ = ttk.Scale
    container = False
    properties = ['class_', 'command', 'cursor', 'from_', 'length',
            'orient', 'style', 'takefocus', 'to', 'variable', 'value',
            'variable']

register('ttk.Scale', TTKScale)


class TTKSeparator(BuilderObject):
    class_ = ttk.Separator
    container = False
    properties = ['class_', 'orient', 'style']

register('ttk.Separator', TTKSeparator)


class TTKLabelframe(BuilderObject):
    class_ = ttk.Labelframe
    container = True
    properties = ['borderwidth', 'class_', 'cursor', 'height',
            'labelanchor', 'labelwidget', 'padding',
            'relief', 'style', 'takefocus', 'text', 'underline', 'width']
#TODO: Add helper so the labelwidget can be configured on GUI
register('ttk.Labelframe', TTKLabelframe)


class TTKPanedwindow(PanedWindow):
    class_ = ttk.Panedwindow
    properties = ['class_', 'cursor', 'height', 'orient',
            'style', 'takefocus', 'width']

register('ttk.Panedwindow', TTKPanedwindow)


class TTKPanedwindowPane(PanedWindowPane):
    class_ = None
    container = True
    properties = ['weight']

register('ttk.Panedwindow.Pane', TTKPanedwindowPane)


class TTKNotebook(BuilderObject):
    class_ = ttk.Notebook
    container = True
    properties = ['class_', 'cursor', 'height',
            'padding', 'style', 'takefocus', 'width']

register('ttk.Notebook', TTKNotebook)


class TTKNotebookTab(BuilderObject):
    class_ = None
    container = True
    properties = ['compound', 'padding', 'sticky',
        'image', 'text', 'underline']

    def __init__(self, master, properties, layout_prop):
        self.widget = master
        self.properties= properties
        self.layout_properties = layout_prop

    def configure(self):
        pass

    def layout(self):
        pass

    def add_child(self, cwidget):
        self.widget.add(cwidget, **self.properties)

register('ttk.Notebook.Tab', TTKNotebookTab)


class TTKMenubutton(BuilderObject):
    class_ = ttk.Menubutton
    container = True
    properties = ['class_', 'compound', 'cursor', 'direction',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'width']

    def add_child(self, cwidget):
        self.widget['menu'] = cwidget

register('ttk.Menubutton', TTKMenubutton)


class TKMenu(BuilderObject):
    class_ = tkinter.Menu
    container = True
    properties = ['activebackground', 'activeborderwidth', 'activeforeground',
        'background', 'borderwidth', 'cursor', 'disabledforeground',
        'font', 'foreground', 'postcommand', 'relief', 'selectcolor',
        'tearoff', 'tearoffcommand', 'title']

    def layout(self):
        pass

register('tk.Menu', TKMenu)


class TKMenuitem(BuilderObject):
    class_ = None
    container = False
    itemtype = None
    #FIXME Move properties that are for specific items to the corresponding
    #  subclass, eg: onvalue, offvalue to checkbutton
    #FIXME Howto setup radio buttons variables ?
    properties = ['accelerator', 'activebackground', 'activeforeground',
        'background', 'bitmap', 'columnbreak', 'command', 'compound',
        'font', 'foreground', 'hidemargin', 'image', 'label',
        'offvalue', 'onvalue', 'selectcolor', 'selectimage', 'state',
        'underline', 'value', 'variable']

    def __init__(self, master, properties, layout_prop):
        self.widget = master
        master.add(self.itemtype, **properties)
        self.properties= properties
        self.layout_properties = layout_prop

    def configure(self):
        pass

    def layout(self):
        pass


class TKMenuitemSubmenu(TKMenu):
    properties = list(set(TKMenu.properties + TKMenuitem.properties))

    def __init__(self, master, properties, layout_prop):
        menu_properties = dict((k, v) for k, v in properties.items()
            if k in TKMenu.properties)

        item_properties = dict((k, v) for k, v in properties.items()
            if k in TKMenuitem.properties)

        self.widget = submenu = TKMenu.class_(master, **menu_properties)
        item_properties['menu'] = submenu
        master.add(tkinter.constants.CASCADE, **item_properties)
        self.properties = properties
        self.layout_properties = layout_prop

    def configure(self):
        pass

    def layout(self):
        pass

register('tk.Menuitem.Submenu', TKMenuitemSubmenu)


class TKMenuitemCommand(TKMenuitem):
    itemtype = tkinter.constants.COMMAND

register('tk.Menuitem.Command', TKMenuitemCommand)


class TKMenuitemCheckbutton(TKMenuitem):
    itemtype = tkinter.constants.CHECKBUTTON

register('tk.Menuitem.Checkbutton', TKMenuitemCheckbutton)


class TKMenuitemRadiobutton(TKMenuitem):
    itemtype = tkinter.constants.RADIOBUTTON

register('tk.Menuitem.Radiobutton', TKMenuitemRadiobutton)


class TKMenuitemSeparator(TKMenuitem):
    itemtype = tkinter.constants.SEPARATOR
    properties = []

register('tk.Menuitem.Separator', TKMenuitemSeparator)


class TTKTreeview(BuilderObject):
    class_ = ttk.Treeview
    container = False
    properties = ['class_', 'cursor', 'height', 'padding', 'selectmode',
        'show', 'style', 'takefocus']
    #FIXME add support to properties: 'columns', 'displaycolumns'
    # and columns properties

register('ttk.Treeview', TTKTreeview)


class TKCanvas(BuilderObject):
    class_ = tkinter.Canvas
    container = False
    properties = ['borderwidth', 'background', 'closeenough', 'confine',
        'cursor', 'height', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'relief', 'scrollregion', 'selectbackground',
        'selectborderwidth', 'selectforeground', 'takefocus', 'width',
        'xscrollincrement', 'xscrollcommand', 'yscrollincrement',
        'yscrollcommand']

register('tk.Canvas', TKCanvas)


def _autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed.
    Code from Joe English (JE) at http://wiki.tcl.tk/950"""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


class ScrollbarHelper(BuilderObject):
    class_ = None
    scrollbar_class = None
    container = True
    properties = ['scrolltype']
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'
    BOTH = 'both'

    def configure(self):
        scrolltype = self.properties.get('scrolltype', self.BOTH)
        if scrolltype in (self.BOTH, self.VERTICAL):
            self.widget.vsb = self.scrollbar_class(self.widget,
                orient="vertical")
            #packing
            self.widget.vsb.grid(column=1, row=0, sticky=tkinter.NS)

        if scrolltype in (self.BOTH, self.HORIZONTAL):
            self.widget.hsb = self.scrollbar_class(self.widget,
                orient="horizontal")
            self.widget.hsb.grid(column=0, row=1, sticky=tkinter.EW)

        self.widget.grid_columnconfigure(0, weight=1)
        self.widget.grid_rowconfigure(0, weight=1)

    def add_child(self, cwidget):
        cwidget.grid(column=0, row=0, sticky=tkinter.NSEW, in_=self.widget)
        scrolltype = self.properties.get('scrolltype', self.BOTH)

        if scrolltype in (self.BOTH, self.VERTICAL):
            self.widget.vsb.configure(command=cwidget.yview)
            cwidget.configure(yscrollcommand=lambda f, l: _autoscroll(self.widget.vsb, f, l))

        if scrolltype in (self.BOTH, self.HORIZONTAL):
            self.widget.hsb.configure(command=cwidget.xview)
            cwidget.configure(xscrollcommand=lambda f, l: _autoscroll(self.widget.hsb, f, l))

__scrolltype_property = {
    'input_method': 'choice',
    'values': (ScrollbarHelper.BOTH, ScrollbarHelper.VERTICAL,
        ScrollbarHelper.HORIZONTAL),
    'default': ScrollbarHelper.BOTH }

register_property('scrolltype', __scrolltype_property)


class TKScrollbarHelper(ScrollbarHelper):
    class_ = tkinter.Frame
    scrollbar_class = tkinter.Scrollbar

register('tk.ScrollbarHelper', TKScrollbarHelper)


class TTKScrollbarHelper(ScrollbarHelper):
    class_ = ttk.Frame
    scrollbar_class = ttk.Scrollbar

register('ttk.ScrollbarHelper', TTKScrollbarHelper)


class ScrolledFrame(BuilderObject):
    class_ = None
    scrollbar_class = None
    container = True
    properties = []

    def __init__(self, master, properties, layout_prop):
        self.properties = properties
        self.layout_properties = layout_prop
        self.widget = self.class_(master)
        self.canvas = canvas = tkinter.Canvas(self.widget, bd=0, highlightthickness=0)
        self.innerframe = innerframe = self.class_(self.canvas)
        self.vsb = vsb = self.scrollbar_class(self.widget)
        self.hsb = hsb = self.scrollbar_class(self.widget, orient="horizontal")
        self.widget.innerframe = innerframe
        self.widget.vsb = vsb
        self.widget.hsb = hsb

        #configure scroll
        self.canvas.configure(
            yscrollcommand=lambda f, l: _autoscroll(vsb, f, l))
        self.canvas.configure(
            xscrollcommand=lambda f, l: _autoscroll(hsb, f, l))
        self.vsb.config(command=canvas.yview)
        self.hsb.config(command=canvas.xview)

        #grid
        self.canvas.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.vsb.grid(row=0, column=1, sticky=tkinter.NS)
        self.hsb.grid(row=1, column=0, sticky=tkinter.EW)
        self.widget.rowconfigure(0, weight=1)
        self.widget.columnconfigure(0, weight=1)

        # create a window inside the canvas which will be scrolled with it
        innerframe_id = canvas.create_window(0, 0, window=innerframe,
            anchor=tkinter.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_innerframe(event):
            # update the scrollbars to match the size of the inner frame
            size = (innerframe.winfo_reqwidth(), innerframe.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if innerframe.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=innerframe.winfo_reqwidth())

        innerframe.bind('<Configure>', _configure_innerframe)

        def _configure_canvas(event):
            if innerframe.winfo_reqwidth() < canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(innerframe_id, width=canvas.winfo_width(),
                    height= canvas.winfo_height())
            if innerframe.winfo_reqheight() < canvas.winfo_height():
                canvas.itemconfigure(
                    innerframe_id, height= canvas.winfo_height())

        canvas.bind('<Configure>', _configure_canvas)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)


    def configure(self):
        pass


    def get_child_master(self):
        return self.innerframe


class TKScrolledFrame(ScrolledFrame):
    class_ = tkinter.Frame
    scrollbar_class = tkinter.Scrollbar

register('tk.ScrolledFrame', TKScrolledFrame)


class TTKScrolledFrame(ScrolledFrame):
    class_ = ttk.Frame
    scrollbar_class = ttk.Scrollbar

register('ttk.ScrolledFrame', TTKScrolledFrame)


#
# Builder class
#

class Builder:
    #TODO: Add a method 'bind' or similar to map commands to a function
    # something like: builder.bind(self)
    def __init__(self):
        self.tree = None
        self.root = None
        self.widgets = {}

    def add_from_file(self, fpath):
        if self.tree is None:
            self.tree = tree = ET.parse(fpath)
            self.root = tree.getroot()
            self.widgets = {}
        else:
            #TODO: append to current tree
            pass


    def add_from_xmlnode(self, element):
        if self.tree is None:
            root = ET.Element('interface')
            root.append(element)
            self.tree = tree = ET.ElementTree(root)
            self.root = tree.getroot()
            self.widgets = {}
            ET.dump(tree)
        else:
            #TODO: append to current tree
            pass


    def get_object(self, name, master=None):
        widget = None
        if name in self.widgets:
            widget = self.widgets[name]
        else:
            xpath = ".//object[@id='{0}']".format(name)
            node = self.tree.find(xpath)
            if node is not None:
                widget = self.realize(master, node)
        if widget is None:
            raise Exception('Widget not defined.')
        return widget


    def realize(self, master, element):
        cname = element.get('class')
        uniqueid = element.get('id')

        if cname in CLASS_MAP:
            properties = self.get_properties(element)
            layout = self.get_layout_properties(element)
            builderobj = CLASS_MAP[cname].factory(master, properties, layout)
            builderobj.configure()
            builderobj.layout()
            pwidget = builderobj.widget

            self.widgets[uniqueid] = pwidget

            xpath = "./child"
            children = element.findall(xpath)
            for child in children:
                child_object = child.find('./object')
                cmaster = builderobj.get_child_master()
                cwidget = self.realize(cmaster, child_object)
                builderobj.add_child(cwidget)

            return pwidget
        else:
            raise Exception('Class "{0}" not mapped'.format(cname))


    def get_layout_properties(self, element):
        #use grid layout for all
        #get packing properties
        layout_properties = {}
        packing_elem = element.find('./packing')
        if packing_elem is not None:
            layout_properties = self.get_properties(packing_elem)

            #get grid row and col properties:
            rows_dict = {}
            erows = packing_elem.find('./rows')
            if erows is not None:
                rows = erows.findall('./row')
                for row in rows:
                    row_id = row.get('id')
                    row_properties = self.get_properties(row)
                    rows_dict[row_id] = row_properties
            layout_properties['grid_rows'] = rows_dict

            columns_dict = {}
            ecolums = packing_elem.find('./columns')
            if ecolums is not None:
                columns = ecolums.findall('./column')
                for column in columns:
                    column_id = column.get('id')
                    column_properties = self.get_properties(column)
                    columns_dict[column_id] = column_properties
            layout_properties['grid_columns'] = columns_dict
        else:
            cname = element.get('class')
            uniqueid = element.get('id')
            logger.warning('No packing information for: (%s, %s).',
                cname, uniqueid)
        return layout_properties


    def get_properties(self, element):
        properties = element.findall('./property')
        pdict= {}
        for p in properties:
            pdict[p.get('name')] = p.text
        return pdict


