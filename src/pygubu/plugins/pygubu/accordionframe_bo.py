# encoding: utf-8
import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from pygubu.widgets.accordionframe import AccordionFrame
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid


class AccordionFrameBO(TTKFrame):
    class_ = AccordionFrame
    allowed_children = (f"{_plugin_uid}.AccordionFrameGroup",)
    _img_properties = ("img_expand", "img_collapse")
    properties = TTKFrame.properties + _img_properties
    tkimage_properties = TTKFrame.tkimage_properties + _img_properties


_builder_uid = f"{_plugin_uid}.AccordionFrame"

register_widget(
    _builder_uid,
    AccordionFrameBO,
    "AccordionFrame",
    (_tab_widgets_label, "ttk"),
)


class AccordionFrameGroupBO(BuilderObject):
    allowed_parents = (f"{_plugin_uid}.AccordionFrame",)
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


_builder_uid = f"{_plugin_uid}.AccordionFrameGroup"

register_widget(
    _builder_uid,
    AccordionFrameGroupBO,
    "AccordionFrame.Group",
    (_tab_widgets_label, "ttk"),
)
