import tkinter as tk

from pygubu.api.v1 import BuilderObject, register_widget
from pygubu.widgets.scrolledframe import ScrolledFrame
from ._config import nspygubu, _section_containers, GCONTAINER


class TTKScrolledFrameBO(BuilderObject):
    class_ = ScrolledFrame
    container = True
    container_layout = True
    #    maxchildren = 1
    #    allowed_children = ('tk.Frame', 'ttk.Frame' )
    OPTIONS_STANDARD = ("class_", "cursor", "takefocus", "style")
    OPTIONS_SPECIFIC = ("borderwidth", "relief", "padding", "height", "width")
    OPTIONS_CUSTOM = ("scrolltype", "usemousewheel")
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = (
        "class_",
        "scrolltype",
    )

    def get_child_master(self):
        return self.widget.innerframe

    def configure(self, target=None):
        super().configure(self.widget.innerframe)

    def _container_layout(self, target, container_manager, properties):
        super()._container_layout(
            self.widget.innerframe, container_manager, properties
        )

    def _set_property(self, target_widget, pname, value):
        if pname in ("usemousewheel",):
            super()._set_property(self.widget, pname, value)
        else:
            super()._set_property(target_widget, pname, value)

    #
    # Code generation methods
    #
    def code_child_master(self):
        return f"{self.code_identifier()}.innerframe"

    def code_configure(self, targetid=None):
        realtarget = f"{self.code_identifier()}.innerframe"
        return super().code_configure(realtarget)

    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == "usemousewheel":
            nvalue = "{}.configure({}={})".format(
                self.code_identifier(), pname, tk.getboolean(value)
            )
            code_bag[pname] = [nvalue]
        else:
            super()._code_set_property(targetid, pname, value, code_bag)


register_widget(
    nspygubu.widgets.ScrolledFrame,
    TTKScrolledFrameBO,
    "ScrolledFrame",
    _section_containers,
    group=GCONTAINER,
)

register_widget(
    nspygubu.builder_old.scrolledframe,
    TTKScrolledFrameBO,
    public=False,
)
