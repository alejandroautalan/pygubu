import tkinter as tk
from typing import Mapping
from TKinterModernThemes.WidgetFrame import WidgetFrame, Notebook, PanedWindow
from pygubu.api.v1 import BuilderObject
from pygubu.utils.datatrans import ListDTO
from .codegen import TkmtWidgetCodeMixin


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
GROUP_ROOT = 0
GROUP_CONTAINER = 10
GROUP_DISPLAY = 30
GROUP_INPUT = 60


class CommandProxy:
    def __init__(self):
        self.command = None

    @property
    def __name__(self):
        return f"CommandProxy({self.command})"

    def __call__(self, *args):
        if self.command is not None:
            self.command(*args)


class TkmtWidgetBO(TkmtWidgetCodeMixin, BuilderObject):
    allow_bindings = False
    layout_required = False
    pos_args = ()
    kw_args = ("row", "col", "padx", "pady", "rowspan", "colspan", "sticky")
    args_to_list = ListDTO([], [])  # To process args property

    def __init__(self, builder, wmeta):
        super().__init__(builder, wmeta)
        self.command_proxies: Mapping[str, CommandProxy] = {}
        self.make_resizable = None

    def realize(self, parent, extra_init_args: dict = None):
        master = parent.get_child_master()
        pbag = self._process_properties(tkmt_to_tkwidget(master))
        kargs = self._get_keyword_args(pbag)
        args = self._get_positional_args(pbag)
        self.widget = self.class_(*args, **kargs)
        return self.widget

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
            if pname in self.kw_args and pname in bag:
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

    def configure(self, target=None):
        if target is None:
            target = self.widget
        for pname, value in self.wmeta.properties.items():
            if pname not in self.pos_args and pname not in self.kw_args:
                self._set_property(target, pname, value)

    def _set_property(self, target_widget, pname, value):
        if pname == "makeResizable":
            self.make_resizable = value
            return
        super()._set_property(target_widget, pname, value)

    def configure_children(self, target=None):
        if target is None:
            target = self.widget
        if self.make_resizable is not None:
            if self.make_resizable == "all":
                target.makeResizable()
            elif self.make_resizable == "recursive":
                target.makeResizable(recursive=True, onlyFrames=False)
            else:
                target.makeResizable(recursive=False, onlyFrames=True)

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
        if pname in ("disabled", "usecommandlineargs", "useconfigfile"):
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def _connect_command(self, cmd_pname, callback):
        self.command_proxies[cmd_pname].command = callback

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname in ("args", "validatecommandargs", "invalidcommandargs"):
            return str(self.args_to_list.transform(value))
        if pname == "variable":
            # variables can be none in some constructors
            # avoid error when builder trys to create a tk variable.
            if value is None:
                return str(value)
        return super()._code_process_property_value(targetid, pname, value)


class WidgetAsMethodBO(TkmtWidgetBO):
    master_add_method = None

    def realize(self, parent, extra_init_args: dict = None):
        master = parent.get_child_master()
        assert self.master_add_method is not None
        add_method = getattr(master, self.master_add_method)
        pbag = self._process_properties(tkmt_to_tkwidget(master))
        kargs = self._get_keyword_args(pbag)
        args = self._get_positional_args(pbag)
        self.widget = add_method(*args, **kargs)
        return self.widget
