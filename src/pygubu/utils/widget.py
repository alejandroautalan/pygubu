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
    if not parent or parent == ".":
        return None
    while top != parent:
        pw = widget.nametowidget(parent)
        yield pw
        parent = pw.winfo_parent()


def iter_to_toplevel(widget: tk.Widget):
    """Iter parents of widget including widget itself"""
    yield widget
    yield from iter_parents(widget)


class HideableMixin:
    """Allows to hide a tk.Widget."""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._is_hidden = None
        self._layout = None
        self._layout_info = None

    @property
    def hidden(self):
        return self._is_hidden

    @hidden.setter
    def hidden(self, state: bool):
        if state:
            self._hide()
        else:
            self._show()

    def _hide(self):
        if self._is_hidden is None:
            self._layout = m = self.winfo_manager()
            if m == "pack":
                self._layout_info = self.pack_info()
                self._layout_info.pop("in", None)
                parent = self.nametowidget(self.winfo_parent())
                wlist = parent.pack_slaves()
                total = len(wlist)
                self_index = wlist.index(self)
                if total > 1:
                    if self_index == 0:
                        self._layout_info["before"] = wlist[1]
                    else:
                        self._layout_info["after"] = wlist[self_index - 1]

            elif m == "place":
                self._layout_info = info = self.place_info()
                info.pop("in", None)
                # FIXME: ttkbootstrap issue with localization ??
                for key in ("relx", "rely", "relwidth", "relheight"):
                    info[key] = str(info[key]).replace(",", ".")
            self._is_hidden = False

        if self._is_hidden is False:
            if self._layout == "pack":
                self.pack_forget()
            elif self._layout == "grid":
                self.grid_remove()
            elif self._layout == "place":
                self.place_forget()
            self._is_hidden = True

    def _show(self):
        if self._is_hidden:
            layout = self._layout
            if layout == "pack":
                self.pack(**self._layout_info)
            elif layout == "grid":
                self.grid()
            elif layout == "place":
                self.place(**self._layout_info)
            self._is_hidden = False
