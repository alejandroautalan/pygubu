""" Widget utility functions."""
import tkinter as tk


def crop_widget(widget, *, recursive=False):
    """Remove standard widget functionality."""

    # Remove standard bindings
    wclass = widget.winfo_class()
    bindtags = widget.bindtags()
    if wclass in bindtags:
        bindtags = list(bindtags)
        bindtags.remove(wclass)
        widget.bindtags(bindtags)
    # Don't take focus
    try:
        widget.configure(takefocus=False)
    except Exception:
        pass

    if recursive:
        for childw in widget.winfo_children():
            crop_widget(childw, recursive=recursive)


def iter_parents(widget: tk.Widget):
    top = str(widget.winfo_toplevel())
    parent = widget.winfo_parent()
    if parent == ".":
        return
    while top != parent:
        pw = widget.nametowidget(parent)
        yield pw
        parent = pw.winfo_parent()


def iter_to_toplevel(widget: tk.Widget):
    """Iter parents of widget including widget itself"""
    yield widget
    yield from iter_parents(widget)
