# encoding: utf-8
import tkinter as tk

from pygubu.api.v1 import BuilderObject, register_widget
from pygubu.i18n import _
from pygubu.widgets.tkscrolledframe import TkScrolledFrame


class TKScrolledFrameBO(BuilderObject):
    class_ = TkScrolledFrame
    container = True
    #    maxchildren = 1
    #    allowed_children = ('tk.Frame', 'ttk.Frame' )
    OPTIONS_STANDARD = (
        "borderwidth",
        "cursor",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "padx",
        "pady",
        "relief",
        "takefocus",
    )
    OPTIONS_SPECIFIC = (
        "background",
        "class_",
        "container",
        "height",
        "width",
    )
    OPTIONS_CUSTOM = ("scrolltype", "usemousewheel")
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = ("class_", "scrolltype")

    def get_child_master(self):
        return self.widget.innerframe

    def configure(self, target=None):
        super(TKScrolledFrameBO, self).configure(self.widget.innerframe)

    def _set_property(self, target_widget, pname, value):
        if pname in ("usemousewheel",):
            super(TKScrolledFrameBO, self)._set_property(
                self.widget, pname, value
            )
        else:
            super(TKScrolledFrameBO, self)._set_property(
                target_widget, pname, value
            )

    #
    # Code generation methods
    #
    def code_child_master(self):
        return "{0}.innerframe".format(self.code_identifier())

    def code_configure(self, targetid=None):
        realtarget = "{0}.innerframe".format(self.code_identifier())
        return super(TKScrolledFrameBO, self).code_configure(realtarget)

    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == "usemousewheel":
            nvalue = "{0}.configure({1}={2})".format(
                self.code_identifier(), pname, tk.getboolean(value)
            )
            code_bag[pname] = [nvalue]
        else:
            super(TKScrolledFrameBO, self)._code_set_property(
                targetid, pname, value, code_bag
            )


register_widget(
    "pygubu.builder.widgets.tkscrolledframe",
    TKScrolledFrameBO,
    "ScrolledFrame",
    (_("Pygubu Widgets"), "tk"),
    group=0,
)
