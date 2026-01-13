# encoding: utf-8
from pygubu.api.v1 import register_widget
from pygubu.plugins.tk.tkstdwidgets import TKToplevel
from pygubu.widgets.dialog import Dialog
from ._config import nspygubu, _designer_tabs_widgets_ttk


class DialogBO(TKToplevel):
    class_ = Dialog
    OPTIONS_STANDARD = TKToplevel.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = TKToplevel.OPTIONS_SPECIFIC
    OPTIONS_CUSTOM = TKToplevel.OPTIONS_CUSTOM + ("modal",)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    virtual_events = ("<<DialogClose>>",)

    def layout(self, target=None, *, forget=False):
        super(DialogBO, self).layout(self.widget.toplevel, forget=forget)

    def _set_property(self, target_widget, pname, value):
        if pname == "modal":
            modal = False
            value = value.lower()
            if value == "true":
                modal = True
            self.widget.set_modal(modal)
        else:
            super(DialogBO, self)._set_property(
                self.widget.toplevel, pname, value
            )

    def get_child_master(self):
        return self.widget.toplevel

    #
    # Code generation methods
    #
    def code_child_master(self):
        return "{0}.toplevel".format(self.code_identifier())

    def _code_set_property(self, targetid, pname, value, code_bag):
        new_target = f"{targetid}.toplevel"
        super(DialogBO, self)._code_set_property(
            new_target, pname, value, code_bag
        )


register_widget(
    nspygubu.widgets.Dialog,
    DialogBO,
    "Dialog",
    _designer_tabs_widgets_ttk,
    group=0,
)
# Register old name until removal
register_widget(nspygubu.builder_old.dialog, DialogBO, public=False)
