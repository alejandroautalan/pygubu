# encoding: utf-8
import logging
import tkinter as tk

from pygubu.binding import (
    ApplicationLevelBindManager as BindManager,
    remove_binding,
)

logger = logging.getLogger(__name__)


def _autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed.
    Code from Joe English (JE) at http://wiki.tcl.tk/950"""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


class ScrollbarHelperBase(object):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    BOTH = "both"
    _framecls = None
    _sbarcls = None

    def __init__(self, master=None, **kw):
        self.scrolltype = kw.pop("scrolltype", self.VERTICAL)
        self.usemousewheel = tk.getboolean(kw.pop("usemousewheel", False))
        super(ScrollbarHelperBase, self).__init__(master, **kw)
        self.vsb = None
        self.hsb = None
        self.cwidget = None
        self.container = c = self._framecls(self)
        c.grid(row=0, column=0, sticky="nsew")
        self._bindingids = []
        self._create_scrollbars()

    def _create_scrollbars(self):
        if self.scrolltype in (self.BOTH, self.VERTICAL):
            self.vsb = self._sbarcls(self, orient="vertical")
            # layout
            self.vsb.grid(column=1, row=0, sticky=tk.NS)

        if self.scrolltype in (self.BOTH, self.HORIZONTAL):
            self.hsb = self._sbarcls(self, orient="horizontal")
            self.hsb.grid(column=0, row=1, sticky=tk.EW)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def add_child(self, cwidget):
        self.cwidget = cwidget
        cwidget.pack(expand=True, fill="both", in_=self.container)

        if self.scrolltype in (self.BOTH, self.VERTICAL):
            if hasattr(cwidget, "yview"):
                self.vsb.configure(command=cwidget.yview)
                cwidget.configure(
                    yscrollcommand=lambda f, l: _autoscroll(self.vsb, f, l)
                )
            else:
                msg = "widget %s has no attribute 'yview'"
                logger.info(msg, str(cwidget))

        if self.scrolltype in (self.BOTH, self.HORIZONTAL):
            if hasattr(cwidget, "xview"):
                self.hsb.configure(command=cwidget.xview)
                cwidget.configure(
                    xscrollcommand=lambda f, l: _autoscroll(self.hsb, f, l)
                )
            else:
                msg = "widget % has no attribute 'xview'"
                logger.info(msg, str(cwidget))
        self._configure_mousewheel()

    def configure(self, cnf=None, **kw):
        if cnf:
            return super().configure(cnf, **kw)
        key = "usemousewheel"
        if key in kw:
            self.usemousewheel = tk.getboolean(kw.pop(key))
            self._configure_mousewheel()
        return super().configure(cnf, **kw)

    config = configure

    def cget(self, key):
        option = "usemousewheel"
        if key == option:
            return self.usemousewheel
        return super(ScrollbarHelperBase, self).cget(key)

    __getitem__ = cget

    def _configure_mousewheel(self):
        cwidget = self.cwidget
        if self.usemousewheel and cwidget is not None:
            BindManager.init_mousewheel_binding(self)

            if self.hsb and not hasattr(self.hsb, "on_mousewheel"):
                self.hsb.on_mousewheel = BindManager.make_onmousewheel_cb(
                    cwidget, "x", 2
                )
            if self.vsb and not hasattr(self.vsb, "on_mousewheel"):
                self.vsb.on_mousewheel = BindManager.make_onmousewheel_cb(
                    cwidget, "y", 2
                )

            main_sb = self.vsb or self.hsb
            if main_sb:
                cwidget.on_mousewheel = main_sb.on_mousewheel
                BindManager.mousewheel_bind(cwidget)
            for s in (self.vsb, self.hsb):
                if s:
                    BindManager.mousewheel_bind(s)
        else:
            for w in (cwidget, self.vsb, self.hsb):
                BindManager.mousewheel_unbind(w)


class ScrollbarHelperFactory(type):
    def __new__(cls, clsname, superclasses, attrs):
        return type.__new__(cls, str(clsname), superclasses, attrs)


TkScrollbarHelper = ScrollbarHelperFactory(
    "TkScrollbarHelper",
    (ScrollbarHelperBase, tk.Frame, object),
    {"_framecls": tk.Frame, "_sbarcls": tk.Scrollbar},
)
