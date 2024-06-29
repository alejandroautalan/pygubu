import tkinter as tk
from typing import Mapping
from TKinterModernThemes.WidgetFrame import WidgetFrame, Notebook, PanedWindow
from pygubu.api.v1 import BuilderObject
from pygubu.utils.datatrans import ListDTO


def tkmt_to_tkwidget(widget):
    """Get underline tk widget."""
    if isinstance(widget, tk.Widget):
        return widget
    if isinstance(widget, WidgetFrame):
        return widget.master
    if isinstance(widget, Notebook):
        return widget.notebook
    if isinstance(widget, PanedWindow):
        return widget.panedwindow
    return None


# Groups for ordering buttons in designer palette.
GROUP_CONTAINER = 0
GROUP_DISPLAY = 1
GROUP_INPUT = 2


class CommandProxy:
    def __init__(self):
        self.command = None

    @property
    def __name__(self):
        return f"CommandProxy({self.command})"

    def __call__(self, *args):
        if self.command is not None:
            self.command(*args)


class TkmtWidgetBO(BuilderObject):
    allow_bindings = False
    layout_required = False
    properties = ("row", "col", "padx", "pady", "rowspan", "colspan", "sticky")
    ro_properties = properties
    pos_args = tuple()
    master_add_method = None
    args_to_list = ListDTO([], [])  # To process args property

    def __init__(self, builder, wmeta):
        super().__init__(builder, wmeta)
        self.command_proxies: Mapping[str, CommandProxy] = {}

    def realize(self, parent, extra_init_args: dict = None):
        master = parent.get_child_master()
        assert self.master_add_method is not None
        add_method = getattr(master, self.master_add_method)
        pbag = self._process_properties(tkmt_to_tkwidget(master))
        kargs = self._get_keyword_args(pbag)
        args = self._get_positional_args(pbag)
        self.widget = add_method(*args, **kargs)
        return self.widget

    def configure(self, target=None):
        pass

    def _process_properties(self, tkmaster: tk.Widget) -> dict:
        defaults = self._get_property_defaults(tkmaster)
        pbag = {}
        for pname in self.properties:
            if pname in self.wmeta.properties:
                pvalue = self.wmeta.properties[pname]
                pbag[pname] = self._process_property_value(pname, pvalue)
            elif pname in defaults:
                pbag[pname] = defaults[pname]
        self._post_process_properties(tkmaster, pbag)
        return pbag

    def _post_process_properties(self, tkmaster: tk.Widget, pbag: dict) -> None:
        pass

    def _get_keyword_args(self, bag: dict) -> dict:
        kargs = {}
        for pname in self.properties:
            if pname not in self.pos_args and pname in bag:
                kargs[pname] = bag[pname]
        return kargs

    def _get_positional_args(self, bag: dict) -> list:
        args = []
        for pname in self.pos_args:
            if pname in bag:
                value = bag[pname]
                args.append(value)
        return args

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {}

    def _set_property(self, target_widget, pname, value):
        if pname == "makeResizable":
            if value == "all":
                target_widget.makeResizable()
            elif value == "recursive":
                target_widget.makeResizable(recursive=True, onlyFrames=False)
            else:
                target_widget.makeResizable(recursive=False, onlyFrames=True)
            return
        super()._set_property(target_widget, pname, value)

    def _process_property_value(self, pname, value):
        if pname in self.command_properties:
            cmd_proxy = self.command_proxies.get(pname, None)
            if cmd_proxy is None:
                cmd_proxy = CommandProxy()
                self.command_proxies[pname] = cmd_proxy
            return cmd_proxy
        if pname in ("row", "col", "rowspan", "colspan"):
            return int(value)
        if pname in ("args", "validatecommandargs", "invalidcommandargs"):
            return self.args_to_list.transform(value)
        if pname in ("disabled",):
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def _connect_command(self, cmd_pname, callback):
        self.command_proxies[cmd_pname].command = callback
