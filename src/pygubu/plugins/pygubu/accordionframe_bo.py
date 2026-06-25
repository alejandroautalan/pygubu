# encoding: utf-8
import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from pygubu.widgets.accordionframe import AccordionFrame
from ._config import nspygubu, _designer_tabs_widgets_ttk, GCONTAINER


class AccordionFrameBO(TTKFrame):
    class_ = AccordionFrame
    allowed_children = (nspygubu.widgets.AccordionFrameGroup,)
    _img_properties = ("img_expand", "img_collapse")
    properties = TTKFrame.properties + _img_properties
    tkimage_properties = TTKFrame.tkimage_properties + _img_properties
    virtual_events = ("<<AccordionGroupToggle>>",)


register_widget(
    nspygubu.widgets.AccordionFrame,
    AccordionFrameBO,
    "AccordionFrame",
    _designer_tabs_widgets_ttk,
    group=GCONTAINER,
)


class AccordionFrameGroupBO(BuilderObject):
    allowed_parents = (nspygubu.widgets.AccordionFrame,)
    properties = ("label", "expanded", "compound", "style")
    layout_required = False
    container = True
    container_layout = True
    allow_bindings = False

    def realize(self, parent, extra_init_args: dict = None):
        args = self._get_init_args(extra_init_args)
        master = parent.get_child_master()
        gid = self.wmeta.identifier
        self.widget = master.add_group(gid, **args)
        self.widget._accordion = parent.widget
        return self.widget

    def _process_property_value(self, pname, value):
        if pname == "expanded":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def _set_property(self, target_widget, pname, value):
        if pname in self.properties:
            propvalue = self._process_property_value(pname, value)
            self.widget._accordion.group_config(
                self.wmeta.identifier, **{pname: propvalue}
            )
        else:
            super()._set_property(target_widget, pname, value)

    #
    # Code generation methods
    #
    def code_realize(self, boparent, code_identifier=None):
        self.parent_bo = boparent
        if code_identifier is not None:
            self._code_identifier = code_identifier
        lines = []
        master = boparent.code_child_master()
        target = self.code_identifier()
        gid_varname = f"{target}_id"
        gid_value = self.wmeta.identifier
        (
            code_bag,
            _ignore,
            _ignore,
        ) = self._code_process_properties(self.wmeta.properties, target)
        kwargs = self.code_make_kwargs_str(code_bag, prefix=", ")
        lines.extend(
            [
                f'{gid_varname} = "{gid_value}"',
                f"{target} = {master}.add_group({gid_varname}{kwargs})",
            ]
        )

        return lines

    def code_configure(self, targetid=None):
        return []


register_widget(
    nspygubu.widgets.AccordionFrameGroup,
    AccordionFrameGroupBO,
    "AccordionFrame.Group",
    _designer_tabs_widgets_ttk,
    group=GCONTAINER,
)
