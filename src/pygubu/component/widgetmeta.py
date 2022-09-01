# encoding: UTF-8
import xml.etree.ElementTree as ET
from collections import namedtuple

from .builderobject import CLASS_MAP

__all__ = ["WidgetMeta", "BindingMeta"]

BindingMeta = namedtuple("BindingMeta", ["sequence", "handler", "add"])

GridRCLine = namedtuple("GridRCLine", ["rctype", "rcid", "pname", "pvalue"])


class WidgetMeta:
    def __init__(
        self,
        cname,
        identifier,
        manager=None,
        properties_defaults=None,
        layout_defaults=None,
    ):
        super().__init__()
        self.classname = cname
        self._id = identifier
        self.properties = {}
        self.bindings = []
        self._manager = manager if manager is not None else "grid"
        widget_description = CLASS_MAP.get(cname)
        if widget_description:
            self.layout_required = widget_description.builder.layout_required
        else:
            self.layout_required = True
        self.layout_properties = {}
        self._container_manager = self._manager
        self.container_properties = {}
        self.gridrc_properties = []
        self.properties_defaults = (
            properties_defaults if properties_defaults is not None else {}
        )
        self.layout_defaults = (
            layout_defaults if layout_defaults is not None else {}
        )
        self._named = False
        # init defaults
        self.apply_properties_defaults()
        self.apply_layout_defaults()

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, value):
        self._manager = value

    @property
    def container_manager(self):
        return self._container_manager

    @container_manager.setter
    def container_manager(self, value):
        if value == "pack" and self.gridrc_properties:
            self.gridrc_properties.clear()
        self._container_manager = value

    @property
    def is_named(self) -> bool:
        return self._named

    @is_named.setter
    def is_named(self, value: bool):
        self._named = value

    @property
    def identifier(self) -> str:
        return self._id

    @identifier.setter
    def identifier(self, value: str):
        if not value:
            raise ValueError()
        self._id = value

    def apply_properties_defaults(self):
        for name, value in self.properties_defaults.items():
            self.properties[name] = value

    def apply_layout_defaults(self):
        layout_defaults_by_manager = self.layout_defaults
        if self.manager in self.layout_defaults:
            layout_defaults_by_manager = self.layout_defaults[self.manager]
        for name, value in layout_defaults_by_manager.items():
            self.layout_properties[name] = value

    def has_layout_defined(self):
        return len(self.layout_properties) > 0

    def clear_layout(self):
        self.layout_properties = {}
        self.gridrc_properties = []
        self.apply_layout_defaults()

    def get_gridrc_value(self, rctype, rcid, pname):
        value = None
        for line in self.gridrc_properties:
            if (
                line.rctype == rctype
                and line.rcid == rcid
                and line.pname == pname
            ):
                value = line.pvalue
                break
        return value

    def set_gridrc_value(self, rctype, rcid, pname, value):
        index = None
        for i, r in enumerate(self.gridrc_properties):
            if r.rctype == rctype and r.rcid == rcid and r.pname == pname:
                index = i
                break
        if index is None:
            # We're setting the grid rc property on this widget for the first time.

            line = GridRCLine(rctype, rcid, pname, value)
            self.gridrc_properties.append(line)
        else:
            # We're updating an existing grid rc property value.

            # Prevent code such as weight='0', uniform='' from showing up
            # in the generated code - it would be redundant.
            if (pname in ("minsize", "pad", "weight") and value == "0") or (
                pname == "uniform" and not value
            ):

                # We found a redundant value
                # '0' or a blank string if it's for the property: uniform

                # Remove the gridrc property
                self.gridrc_properties.pop(index)
            else:
                # Update the gridrc property
                line = GridRCLine(rctype, rcid, pname, value)
                self.gridrc_properties[index] = line

    def __repr__(self):
        tpl = """<WidgetMeta classname: {0} identifier: {1}>"""
        return tpl.format(self.classname, self.identifier)

    def copy_gridrc(self, from_, rctype):
        """Copy gridrc lines of type rctype from from_"""
        rc = [line for line in self.gridrc_properties if line.rctype != rctype]
        for line in from_.gridrc_properties:
            if line.rctype == rctype:
                rc.append(line)
        self.gridrc_properties = rc

    def copy_properties(self, wfrom):
        # Used on preview methods
        self.properties = wfrom.properties.copy()
        self.gridrc_properties.clear()
        self.gridrc_properties.extend(wfrom.gridrc_properties)
        self.container_manager = wfrom.container_manager
        self.container_properties = wfrom.container_properties


if __name__ == "__main__":
    w = WidgetMeta("mywidget", "w1")
    w.manager = "pack"
    w.properties = {"key1": "value1", "key2": "value2"}
    w.bindings = [
        BindingMeta("<<event_1>>", "callback_1", ""),
        BindingMeta("<<event_2>>", "callback_2", "+"),
    ]
    w.layout_properties = {"prop1": "value1", "prop2": "value2"}

    print("To xml")
    node = w.to_xmlnode()
    node = ET.tostring(node)
    print(node, end="\n\n")

    print("From xml:")
    strdata = """<?xml version='1.0' encoding='utf-8'?>
<object class="ttk.Label" id="Label_1">
        <property name="text" translatable="yes">Label_1</property>
        <property name="background">yellow</property>
        <layout manager="grid">
          <property name="propagate">True</property>
          <property type="row" id="0" name="pad">20</property>
          <property type="col" id="0" name="pad">10</property>
          <property type="row" id="0" name="weight">1</property>
        </layout>
      </object>
    """
    node = ET.fromstring(strdata)
    meta = WidgetMeta.from_xmlnode(node)
    print(meta)
