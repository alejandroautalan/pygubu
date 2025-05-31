# encoding: UTF-8
import json
import operator
import sys
import xml.etree.ElementTree as ET

from .builderobject import CLASS_MAP, TRANSLATABLE_PROPERTIES
from .widgetmeta import BindingMeta, GridRCLine, WidgetMeta


# in-place prettyprint formatter
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:  # Python 2
    JSONDecodeError = ValueError


class UIDefinition(object):
    TK_COMMAND_PROPERTIES = (
        "command",
        "validatecommand",
        "invalidcommand",
        "postcommand",
        "xscrollcommand",
        "yscrollcommand",
        "tearoffcommand",
    )

    def __init__(self, wmetaclass=None, translator=None, author=None):
        super(UIDefinition, self).__init__()
        self.tree = None
        self.root = None
        self._latest_version = "1.4"
        self.version = self._latest_version
        self.author = "" if author is None else author
        self._ignore_properties = (
            "command_id_arg",
            "idtocommand",
            "validatecommand_args",
            "invalidcommand_args",
        )
        self.wmetaclass = wmetaclass
        if wmetaclass is None:
            self.wmetaclass = WidgetMeta
        self.translator = translator
        self.project_node = None
        self._project_settings = {}
        self._custom_widgets = []
        self.uifile = None
        self.__create()

    @property
    def custom_widgets(self) -> list:
        return self._custom_widgets

    @custom_widgets.setter
    def custom_widgets(self, values: list):
        self._custom_widgets = values

    def _load_custom_widgets(self):
        xpath = "./customwidgets/customwidget"
        node_list: ET.Element = self.project_node.findall(xpath)
        if node_list is not None:
            for node in node_list:
                self._custom_widgets.append(node.attrib["path"])

    def _save_custom_widgets(self):
        xpath = "./customwidgets"
        node: ET.Element = self.project_node.find(xpath)
        if node is None:
            node = ET.Element("customwidgets")
            self.project_node.append(node)
        node.clear()
        for value in self._custom_widgets:
            cnode = ET.Element("customwidget")
            cnode.attrib["path"] = str(value)
            node.append(cnode)

    @property
    def project_settings(self) -> dict:
        return self._project_settings

    @project_settings.setter
    def project_settings(self, bag: dict):
        self._project_settings = bag

    def _load_project_settings(self):
        xpath = "./settings/setting"
        node_list: ET.Element = self.project_node.findall(xpath)
        if node_list is not None:
            for node in node_list:
                self._project_settings[node.attrib["id"]] = node.text

    def _save_project_settings(self):
        xpath = ".//settings"
        node: ET.Element = self.project_node.find(xpath)
        if node is None:
            node = ET.Element("settings")
            self.project_node.append(node)
        node.clear()
        for key, value in self._project_settings.items():
            child = ET.Element("setting")
            child.attrib["id"] = str(key)
            if value is not None:
                child.text = str(value)
            node.append(child)

    def _prop_from_xml(self, pnode, element):
        pname = pnode.get("name")
        pvalue = pnode.text

        if pname in self._ignore_properties:
            return (None, None)

        if self.translator is not None and pnode.get("translatable"):
            pvalue = self.translator(pvalue)

        # if node has a type property, send value as a json string
        jvalue = {}
        if pnode.get("type"):
            for attr, attrval in pnode.items():
                jvalue[attr] = attrval
            jvalue["value"] = pnode.text
            pvalue = json.dumps(jvalue)
        # Process old ui versions
        if self.version < "1.1":
            if pname in self.TK_COMMAND_PROPERTIES:
                cmd = {
                    "type": "command",
                    "value": pnode.text,
                    "cbtype": "simple",
                    "args": "",
                }
                # get old format value
                xpath = "./property[@name='{0}']"
                for oldp in ("command_id_arg", "idtocommand"):
                    dpath = xpath.format(oldp)
                    node = element.find(dpath)
                    if node is not None:
                        nvalue = node.text.lower()
                        if nvalue == "true":
                            cmd["cbtype"] = "with_wid"

                if pname in ("validatecommand", "invalidcommand"):
                    cmd["cbtype"] = "entry_validate"
                    # get old format args
                    pargs = "{0}_args".format(pname)
                    dpath = xpath.format(pargs)
                    node = element.find(dpath)
                    if node is not None:
                        cmd["args"] = node.text
                pvalue = json.dumps(cmd)
        return (pname, pvalue)

    def xmlnode_to_widget(self, element):
        elemid = element.get("id")
        meta = self.wmetaclass(element.get("class"), elemid)
        meta.is_named = True if element.get("named") is not None else False

        # properties
        properties = element.findall("./property")
        pdict = {}
        for p in properties:
            pname, pvalue = self._prop_from_xml(p, element)
            if pname is not None:
                pdict[pname] = pvalue

        meta.properties = pdict

        # Bindings
        bindings = []
        bind_elements = element.findall("./bind")
        for e in bind_elements:
            binding = BindingMeta(
                e.get("sequence"), e.get("handler"), e.get("add")
            )
            bindings.append(binding)
        meta.bindings = bindings

        #
        # Load widget layout configuration
        #
        if self.version >= "1.2":
            self.__load_layout_v1_2(element, meta)
        elif self.version >= "1.0":
            self.__load_layout_v1_0(element, meta)
        else:
            self.__load_layout_v_empty(element, meta)

        return meta

    def __load_layout_v1_2(self, element, meta):
        # new 1.2 version
        # layout properties
        # use grid layout by default
        manager = "grid"
        layout_elem = element.find("./layout")
        if layout_elem is not None:
            manager = layout_elem.get("manager", "grid")
            meta.manager = manager
            props = layout_elem.findall("./property")
            for p in props:
                meta.layout_properties[p.get("name")] = p.text

        #
        # Load widget as container layout configuration
        #
        clayout_node = element.find("./containerlayout")
        if clayout_node is not None:
            cmanager = clayout_node.get("manager", None)
            meta.container_manager = cmanager
            props = clayout_node.findall("./property")
            for p in props:
                ptype = p.get("type", None)
                pname = p.get("name")
                if ptype is None:
                    # its a regular container property
                    meta.container_properties[pname] = p.text
                else:
                    # GRID RC PROPERTY
                    pvalue = (
                        "" if p.text is None else p.text
                    )  # fix malformed xml saved
                    line = GridRCLine(ptype, p.get("id"), pname, pvalue)
                    meta.gridrc_properties.append(line)

    def __load_layout_v1_0(self, element, meta):
        # use grid layout by default
        manager = "grid"
        layout_elem = element.find("./layout")
        if layout_elem is not None:
            manager = layout_elem.get("manager", "grid")
            meta.manager = manager
            props = layout_elem.findall("./property")
            for p in props:
                ptype = p.get("type", None)
                pname = p.get("name")
                if ptype is not None:
                    # Its a grid rc, ignore it. Allready loaded in parent.
                    continue
                if pname == "propagate":
                    # don't load if is true. Its the default.
                    # avoid generating an extra containerlayout node
                    # when loading old file versions.
                    value = p.text
                    if value.lower() != "true":
                        meta.container_properties[pname] = p.text
                else:
                    meta.layout_properties[pname] = p.text
            # Try to setup:
            #   - container_manager
            #   - gridrc properties. gridrc properties are on the children.
            child_layouts = element.findall("./child/object/layout")
            rclines_loaded = set()
            if child_layouts is not None:
                clmanager = self._handle_child_layouts(
                    meta, child_layouts, rclines_loaded
                )
            meta.container_manager = clmanager

    def _handle_child_layouts(self, meta, child_layouts, rclines_loaded):
        clmanager = "grid"
        for layout_node in child_layouts:
            manager = layout_node.get("manager", "grid")
            if manager != "place":
                clmanager = manager
            props = layout_node.findall("./property")
            if props is not None:
                for p in props:
                    ptype = p.get("type", None)
                    if ptype is not None:
                        rcid = p.get("id")
                        rcname = p.get("name")
                        key = (ptype, rcid, rcname)
                        if key not in rclines_loaded:
                            rcvalue = p.text
                            line = GridRCLine(ptype, rcid, rcname, rcvalue)
                            meta.gridrc_properties.append(line)
                            rclines_loaded.add(key)
        return clmanager

    def __load_layout_v_empty(self, element, meta):
        """Load layout with ui version empty."""
        elemid = element.get("id")

        parent_has_layout = False
        parent_layout = None

        xpath = ".//*[@id='{0}']/../..".format(elemid)
        parent = self.root.find(xpath)
        if parent is not None:
            parent_layout = parent.find("./layout")
            if parent_layout is not None:
                parent_has_layout = True

        # layout properties
        # use grid layout by default
        manager = "grid"
        layout_elem = element.find("./layout")
        if layout_elem is not None:
            meta.manager = manager
            props = layout_elem.findall("./property")
            for p in props:
                pname = p.get("name")
                if pname == "propagate":
                    # don't load if is true. Its the default.
                    # avoid generating an extra containerlayout node
                    # when loading old file versions.
                    value = p.text
                    if value.lower() != "true":
                        meta.container_properties[pname] = p.text
                else:
                    meta.layout_properties[pname] = p.text

        # try to load old version grid rc info
        # Gridrc info was in the parent, or
        # in the widget itself if has no parent.
        if not parent_has_layout and layout_elem is not None:
            self.__load_old_gridrc_layout(layout_elem, meta)

    def __load_old_gridrc_layout(self, element, meta):
        """Load old grid rc information."""

        rows = element.findall("./rows/row")
        for row in rows:
            rid = row.get("id")
            props = row.findall("./property")
            for p in props:
                rpname = p.get("name")
                rpvalue = p.text
                line = GridRCLine("row", rid, rpname, rpvalue)
                meta.gridrc_properties.append(line)
        columns = element.findall("./columns/column")
        for col in columns:
            cid = col.get("id")
            props = col.findall("./property")
            for p in props:
                cpname = p.get("name")
                cpvalue = p.text
                line = GridRCLine("col", cid, cpname, cpvalue)
                meta.gridrc_properties.append(line)

    def _prop_to_xml(self, pname, pvalue):
        pnode = ET.Element("property")
        pnode.set("name", pname)
        pnode.text = pvalue
        if pname in TRANSLATABLE_PROPERTIES:
            pnode.set("translatable", "yes")
        # if pvalue is a json do special
        try:
            dv = json.loads(pvalue)
            if isinstance(dv, dict):
                if "value" not in dv:
                    raise Exception("Invalid json value for property")
                for k, attrval in dv.items():
                    if k != "value":
                        pnode.set(k, str(attrval))
                pnode.text = dv["value"]
        except (JSONDecodeError, TypeError):
            pass

        return pnode

    def widget_to_xmlnode(self, wmeta):
        """Returns xml representation of widget"""

        node = ET.Element("object")

        node.set("class", wmeta.classname)
        node.set("id", wmeta.identifier)
        if wmeta.is_named:
            node.set("named", str(wmeta.is_named))

        pkeys = sorted(wmeta.properties.keys())
        for pkey in pkeys:
            pnode = self._prop_to_xml(pkey, wmeta.properties[pkey])
            node.append(pnode)

        # bindings:
        bindings = sorted(wmeta.bindings, key=operator.itemgetter(0, 1))
        for b in bindings:
            bind = ET.Element("bind")
            for key in b._fields:
                bind.set(key, getattr(b, key))
            node.append(bind)

        # layout:
        layout_required = CLASS_MAP[wmeta.classname].builder.layout_required
        if layout_required:
            # create layout node
            layout_node = ET.Element("layout")
            layout_node.set("manager", wmeta.manager)

            keys = sorted(wmeta.layout_properties)
            for prop in keys:
                pnode = ET.Element("property")
                pnode.set("name", prop)
                pnode.text = wmeta.layout_properties[prop]
                layout_node.append(pnode)
            # Append node layout
            node.append(layout_node)

        # Container layout properties
        container_layout_required = (
            wmeta.container_properties or wmeta.gridrc_properties
        )
        if container_layout_required:
            # create layout node
            clnode = ET.Element("containerlayout")
            clnode.set("manager", wmeta.container_manager)

            keys = sorted(wmeta.container_properties)
            for prop in keys:
                pnode = ET.Element("property")
                pnode.set("name", prop)
                pnode.text = wmeta.container_properties[prop]
                clnode.append(pnode)

            lines = sorted(
                wmeta.gridrc_properties, key=operator.itemgetter(0, 1, 2)
            )
            for line in lines:
                p = ET.Element("property")
                p.set("type", line.rctype)
                p.set("id", line.rcid)
                p.set("name", line.pname)
                p.text = line.pvalue
                clnode.append(p)
            # Append container layout node
            node.append(clnode)

        return node

    def __create(self):
        # Version 1.0: start of schema versioning, implements multiple layout managers
        # Version 1.1: remove idtocommand and command_id_arg properties
        # Version 1.4: new project structure.
        self.root = root = ET.Element("interface")
        root.set("version", self._latest_version)
        if self.author:
            root.set("author", self.author)
        self.project_node = ET.Element("project")
        root.append(self.project_node)
        self.tree = ET.ElementTree(root)

    def _tree_load(self, tree, default_version=None):
        if default_version is None:
            default_version = ""
        self.tree = tree
        root: ET.Element = tree.getroot()
        version = root.get("version", default_version)
        author = root.get("author", "")
        self.root = root
        self.version = version
        self.author = author
        self.project_node = root.find("./project")
        if self.project_node is None:
            self.project_node = ET.Element("project")
            root.append(self.project_node)
        self._load_project_settings()
        self._load_custom_widgets()

    def load_file(self, file_or_filename):
        tree = ET.parse(file_or_filename)
        self._tree_load(tree)
        self.uifile = file_or_filename

    def load_from_string(self, source, version=None):
        tree = ET.ElementTree(ET.fromstring(source))
        self._tree_load(tree, version)

    def get_xmlnode(self, identifier):
        xpath = ".//object[@id='{0}']".format(identifier)
        node = self.tree.find(xpath)
        return node

    def add_xmlnode(self, node, parent=None):
        if parent is None:
            self.root.append(node)
        else:
            parent.append(node)
        return node

    def add_xmlchild(self, parent, node):
        child = ET.Element("child")
        child.append(node)
        parent.append(child)

    def __str__(self):
        encoding = "unicode"
        return ET.tostring(self.root, encoding=encoding)

    def __repr__(self):
        return '<UIFile xml="{0}">'.format(self.__str__())

    def save(self, file_or_filename):
        self._save_project_settings()
        self._save_custom_widgets()
        indent(self.root)
        self.tree.write(
            file_or_filename, xml_declaration=True, encoding="utf-8"
        )

    def get_widget(self, identifier):
        wmeta = None
        xpath = ".//object[@id='{0}']".format(identifier)
        node = self.tree.find(xpath)
        if node is not None:
            wmeta = self.xmlnode_to_widget(node)
        return wmeta

    def widgets(self):
        xpath = "./object"
        children = self.root.findall(xpath)
        for child in children:
            wmeta = self.xmlnode_to_widget(child)
            yield wmeta

    def widget_children(self, identifier):
        xpath = ".//object[@id='{0}']".format(identifier)
        node = self.tree.find(xpath)
        if node is not None:
            xpath = "./child/object"
            children = node.findall(xpath)
            for child in children:
                wmeta = self.xmlnode_to_widget(child)
                yield wmeta

    def replace_widget(self, identifier, rootmeta):
        xpath = ".//object[@id='{0}']".format(identifier)
        parent = self.root.find(xpath + "/..")
        target = parent.find(xpath)

        if parent is not None:
            # found something
            parent.remove(target)
            replacement = self.widget_to_xmlnode(rootmeta)
            xpath = "./child/object"
            children = target.findall(xpath)
            for child in children:
                self.add_xmlchild(replacement, child)
            if parent.tag == "interface":
                parent.append(replacement)
            else:
                self.add_xmlchild(parent, replacement)


if __name__ == "__main__":
    ui = UIDefinition()
    ui.author = "Module test"
    print(ui)

    xml = """<?xml version='1.0' encoding='utf-8'?>
<interface author="anonymous">
</interface>
"""
    ui.load_from_string(xml)
    print(ui, ui.author, ui.version)

    print("Iterating file:")
    fname = "managers.ui"
    ui.load_file(fname)

    def print_widgets(w):
        print(w)
        for cw in ui.widget_children(w.identifier):
            print_widgets(cw)

    for w in ui.widgets():
        print_widgets(w)
