import types
import tkinter as tk
from tkinter import ttk

from ..builderobject import *


def _autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed.
    Code from Joe English (JE) at http://wiki.tcl.tk/950"""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


class ScrolledFrame(BuilderObject):
    class_ = None
    scrollbar_class = None
    container = True
    properties = []

    def realize(self, master):
        self.widget = self.class_(master)
        self.canvas = canvas = tk.Canvas(self.widget, bd=0, highlightthickness=0)
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
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.vsb.grid(row=0, column=1, sticky=tk.NS)
        self.hsb.grid(row=1, column=0, sticky=tk.EW)
        self.widget.rowconfigure(0, weight=1)
        self.widget.columnconfigure(0, weight=1)

        # create a window inside the canvas which will be scrolled with it
        innerframe_id = canvas.create_window(0, 0, window=innerframe,
            anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_sframe(event):
            size = (innerframe.winfo_reqwidth(), innerframe.winfo_reqheight())
            if innerframe.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=innerframe.winfo_reqwidth())
            if innerframe.winfo_height() != innerframe.winfo_reqheight():
                canvas.itemconfigure(
                    innerframe_id, height=innerframe.winfo_reqheight())

            if innerframe.winfo_reqwidth() < canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(innerframe_id, width=canvas.winfo_width())
            if innerframe.winfo_reqheight() < canvas.winfo_height():
                canvas.itemconfigure(
                    innerframe_id, height= canvas.winfo_height())

            canvas.config(scrollregion="0 0 %s %s" % size)

        innerframe.bind('<Configure>', _configure_sframe)
        canvas.bind('<Configure>', _configure_sframe)

        def reposition(self):
            """This method should be called when children are added,
            removed, grid_remove, and grided in the scrolled frame."""
            self.innerframe.update()
            self.after_idle(_configure_sframe, None)

        self.widget.reposition = types.MethodType(reposition, self.widget)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        return self.widget


    def configure(self):
        mainwidget = self.widget
        self.widget = self.innerframe
        super(ScrolledFrame, self).configure()
        self.widget = mainwidget


    def get_child_master(self):
        return self.innerframe


class TTKScrolledFrame(ScrolledFrame):
    class_ = ttk.Frame
    scrollbar_class = ttk.Scrollbar
    properties = ['class_', 'cursor', 'height', 'padding',
            'relief', 'style', 'takefocus', 'width']
    ro_properties = ro_properties = ('class_',)

register_widget('pygubu.widgets.scrolledframe', TTKScrolledFrame,
    'ScrolledFrame', ('Pygubu Utilities', 'ttk'))

