import tkinter as tk

from pygubu.api.v1 import BuilderObject, register_widget
from pygubu.plugins.ttk.ttkstdwidgets import TTKNotebookTab
from tkinterweb.utilities import Notebook, ColourSelector
from ..tkinterweb import _designer_tab_label, _plugin_uid


class NotebookBO(BuilderObject):
    class_ = Notebook
    container = True
    container_layout = True
    ro_properties = ("class_", "takefocus")
    properties = (
        # ttk.Frame properties:
        "class_",
        "cursor",
        "style",
        "borderwidth",
        "relief",
        "padding",
        "height",
        "width",
    )
    virtual_events = ("<<NotebookTabChanged>>",)


_builder_uid = f"{_plugin_uid}.Notebook"
_notebook_uid = _builder_uid
register_widget(
    _builder_uid, NotebookBO, "Notebook", ("ttk", _designer_tab_label), group=1
)


class NotebookPageBO(TTKNotebookTab):
    allowed_parents = (_notebook_uid,)
    children_layout_override = True
    properties = (
        "state",
        "text",
        "image",
        "compound",
        "underline",
    )


_builder_uid = f"{_plugin_uid}.Notebook.Page"
NotebookBO.add_allowed_child(_builder_uid)

register_widget(
    _builder_uid,
    NotebookPageBO,
    "Notebook.Page",
    ("ttk", _designer_tab_label),
    group=1,
)


class ColourSelectorBO(BuilderObject):
    class_ = ColourSelector
    properties = ("colour",)
    ro_properties = ("colour",)
    virtual_events = ("<<Modified>>",)


_builder_uid = f"{_plugin_uid}.ColourSelector"
register_widget(
    _builder_uid,
    ColourSelectorBO,
    "ColourSelector",
    ("ttk", _designer_tab_label),
    group=2,
)
