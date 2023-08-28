import tkinter as tk
import tkinter.ttk as ttk

from pygubu.api.v1 import (
    register_widget,
    register_custom_property,
    BuilderObject,
)
from pygubu.i18n import _

import pygubu.widgets.dockfw.dockframes as dockingfw


class DockFrameBO(BuilderObject):
    class_ = dockingfw.DockFrame
    container = True
    container_layout = False
    maxchildren = 1

    def get_child_master(self):
        return self.widget.fcenter

    def add_child(self, bobject):
        bobject.widget.pack(expand=True, fill=tk.BOTH)


_builder_id = "pygubu.widgets.dockframe"
register_widget(
    _builder_id, DockFrameBO, "DockFrame", ("ttk", _("Pygubu Widgets"))
)


class DockPaneBO(BuilderObject):
    class_ = dockingfw.DockPane
    container = True
    container_layout = False
    layout_required = False
    properties = ("orient",)
    ro_properties = properties

    @classmethod
    def canbe_child_of(cls, parent_builder, classname):
        allowed = False
        if parent_builder in (DockFrameBO, DockPaneBO):
            allowed = True
        print("canbe_child", parent_builder, classname, allowed)
        return allowed

    def add_child(self, bobject):
        if isinstance(bobject.widget, dockingfw.DockPane):
            print(f"Adding Dockpane: {bobject.widget}")
            self.widget.panedw.add(bobject.widget, weight=1)
        else:
            print(f"Adding Notebook for: {bobject.widget}")
            nb = ttk.Notebook(self.widget)
            self.widget.panedw.add(nb, weight=1)
            nb.add(bobject.widget, text=bobject.wmeta.identifier, sticky="nsew")
            dockingfw.DockingFramework.raise_tree(nb)


_builder_id = "pygubu.widgets.dockpane"
register_widget(
    _builder_id, DockPaneBO, "DockPane", ("ttk", _("Pygubu Widgets"))
)


class DockTabBO(BuilderObject):
    class_ = dockingfw.DockTab
    container = True
    container_layout = True
    layout_required = False

    @classmethod
    def canbe_child_of(cls, parent_builder, classname):
        allowed = False
        if parent_builder is DockPaneBO:
            allowed = True
        print("canbe_child", parent_builder, classname, allowed)
        return allowed

    def get_child_master(self):
        return self.widget.fcenter


_builder_id = "pygubu.widgets.docktab"
register_widget(_builder_id, DockTabBO, "DockTab", ("ttk", _("Pygubu Widgets")))
