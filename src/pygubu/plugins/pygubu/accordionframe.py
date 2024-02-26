# encoding: utf-8
import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from pygubu.i18n import _
from pygubu.widgets.accordionframe import AccordionFrame


class AccordionFrameBO(TTKFrame):
    class_ = AccordionFrame
    allowed_children = ("pygubu.widgets.AccordionFrameGroup",)
    _img_properties = ("img_expand", "img_collapse")
    properties = TTKFrame.properties + _img_properties
    tkimage_properties = TTKFrame.tkimage_properties + _img_properties


_builder_uid = "pygubu.widgets.AccordionFrame"

register_widget(
    _builder_uid,
    AccordionFrameBO,
    "AccordionFrame",
    (_("Pygubu Widgets"), "ttk"),
)

for prop in AccordionFrameBO._img_properties:
    register_custom_property(_builder_uid, prop, "imageentry")


class AccordionFrameGroupBO(BuilderObject):
    allowed_parents = ("pygubu.widgets.AccordionFrame",)
    properties = ("label", "expanded", "compound", "style")
    layout_required = False
    container = True
    container_layout = True
    allow_bindings = False

    def realize(self, parent, extra_init_args: dict = None):
        args = self._get_init_args(extra_init_args)
        master = parent.get_child_master()
        self._accordion = parent.widget
        gid = self.wmeta.identifier
        self.widget = master.add_group(gid, **args)
        return self.widget

    def _process_property_value(self, pname, value):
        if pname == "expanded":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def _set_property(self, target_widget, pname, value):
        if pname in self.properties:
            propvalue = self._process_property_value(pname, value)
            self._accordion.group_config(
                self.wmeta.identifier, **{pname: propvalue}
            )
        else:
            super()._set_property(target_widget, pname, value)


_builder_uid = "pygubu.widgets.AccordionFrameGroup"

register_widget(
    _builder_uid,
    AccordionFrameGroupBO,
    "AccordionFrame.Group",
    (_("Pygubu Widgets"), "ttk"),
)

register_custom_property(_builder_uid, "label", "entry")
register_custom_property(
    _builder_uid, "style", "ttkstylechoice", default_value="Toolbutton"
)
register_custom_property(
    _builder_uid,
    "expanded",
    "choice",
    values=("", "false", "true"),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "compound",
    "choice",
    values=(
        "",
        tk.LEFT,
        tk.RIGHT,
        tk.NONE,
    ),
    state="readonly",
)
