# encoding: utf-8
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.tk.tkstdwidgets import TKToplevel
from pygubu.i18n import _
from pygubu.widgets.dialog import Dialog


class DialogBO(TKToplevel):
    class_ = Dialog
    OPTIONS_STANDARD = TKToplevel.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = TKToplevel.OPTIONS_SPECIFIC
    OPTIONS_CUSTOM = TKToplevel.OPTIONS_CUSTOM + ("modal",)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    virtual_events = ("<<DialogClose>>",)

    def layout(self, target=None):
        super(DialogBO, self).layout(self.widget.toplevel)

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
        if pname == "modal":
            code_bag[pname] = '"{0}"'.format(value)
        else:
            super(DialogBO, self)._code_set_property(
                targetid, pname, value, code_bag
            )


_builder_id = "pygubu.builder.widgets.dialog"
register_widget(
    _builder_id, DialogBO, "Dialog", (_("Pygubu Widgets"), "ttk"), group=0
)

_help = _("Determines if dialog is run in normal or modal mode.")
register_custom_property(
    _builder_id,
    "modal",
    "choice",
    values=("true", "false"),
    state="readonly",
    help=_help,
)
