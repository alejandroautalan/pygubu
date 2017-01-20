# encoding: UTF-8
#
# Copyright 2012-2013 Alejandro Autalán
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import os
import xml.etree.ElementTree as ET
from collections import Counter
import logging
try:
    import tkinter as tk
except:
    import Tkinter as tk

from pygubu import builder
from pygubu.stockimage import StockImage, StockImageException
from . import properties
from .widgeteditor import WidgetEditor
from .widgetdescr import WidgetDescr
from .i18n import translator as _


logger = logging.getLogger('pygubu.designer')


class WidgetsTreeEditor(object):
    GRID_UP = 0
    GRID_DOWN = 1
    GRID_LEFT = 2
    GRID_RIGHT = 3

    def __init__(self, app):
        self.app = app
        self.treeview = app.treeview
        self.previewer = app.previewer
        self.treedata = {}
        self.counter = Counter()
        # Filter vars
        self.filter_on = False
        self.filtervar = app.builder.get_variable('filtervar')
        self.filter_btn = app.builder.get_object('filterclear_btn')
        self.filter_prev_value = ''
        self.filter_prev_sitem = None
        self._detached = []

        self.config_treeview()
        self.config_filter()

        # Widget Editor
        pframe = app.builder.get_object('propertiesframe')
        lframe = app.builder.get_object('layoutframe')
        bindingstree = app.builder.get_object('bindingstree')
        self.widget_editor = WidgetEditor(pframe, lframe, bindingstree)

    def config_filter(self):
        def on_filtervar_changed(varname, element, mode):
            self.filter_by(self.filtervar.get())

        self.filtervar.trace('w', on_filtervar_changed)

        def on_filterbtn_click():
            self.filtervar.set('')

        self.filter_btn.configure(command=on_filterbtn_click)

    def config_treeview(self):
        """Sets treeview columns and other params"""
        tree = self.treeview
        tree.bind('<Double-1>', self.on_treeview_double_click)
        tree.bind('<<TreeviewSelect>>', self.on_treeview_select, add='+')

    def get_toplevel_parent(self, treeitem):
        """Returns the top level parent for treeitem."""
        tv = self.treeview
        toplevel_items = tv.get_children()

        item = treeitem
        while not (item in toplevel_items):
            item = tv.parent(item)

        return item

    def draw_widget(self, item):
        """Create a preview of the selected treeview item"""
        if item:
            self.filter_remove(remember=True)
            selected_id = self.treedata[item]['id']
            item = self.get_toplevel_parent(item)
            widget_id = self.treedata[item]['id']
            wclass = self.treedata[item]['class']
            xmlnode = self.tree_node_to_xml('', item)
            self.previewer.draw(item, widget_id, xmlnode, wclass)
            self.previewer.show_selected(item, selected_id)
            self.filter_restore()

    def preview_in_toplevel(self):
        tv = self.treeview
        sel = tv.selection()
        if sel:
            self.filter_remove(remember=True)
            item = sel[0]
            item = self.get_toplevel_parent(item)
            widget_id = self.treedata[item]['id']
            wclass = self.treedata[item]['class']
            xmlnode = self.tree_node_to_xml('', item)
            self.previewer.preview_in_toplevel(item, widget_id, xmlnode)
            self.filter_restore()
        else:
            logger.warning(_('No item selected.'))

    def on_treeview_double_click(self, event):
        tv = self.treeview
        sel = tv.selection()
        # toplevel_items = tv.get_children()
        if sel:
            item = sel[0]
            if tv.parent(item) == '':
                # only redraw if toplevel is double clicked
                self.draw_widget(item)

    def on_treeview_delete_selection(self, event=None):
        """Removes selected items from treeview"""

        tv = self.treeview
        selection = tv.selection()

        # Need to remove filter
        self.filter_remove(remember=True)

        toplevel_items = tv.get_children()
        parents_to_redraw = set()
        for item in selection:
            try:
                parent = ''
                if item not in toplevel_items:
                    parent = self.get_toplevel_parent(item)
                else:
                    self.previewer.delete(item)
                del self.treedata[item]
                tv.delete(item)
                self.app.set_changed()
                if parent:
                    self._update_max_grid_rc(parent)
                    parents_to_redraw.add(parent)
                self.widget_editor.hide_all()
            except tk.TclError:
                # Selection of parent and child items ??
                # TODO: notify something here
                pass
        # redraw widgets
        for item in parents_to_redraw:
            self.draw_widget(item)
        # restore filter
        self.filter_restore()

    def tree_to_xml(self):
        """Traverses treeview and generates a ElementTree object"""

        # Need to remove filter or hidden items will not be saved.
        self.filter_remove(remember=True)

        tree = self.treeview
        root = ET.Element('interface')
        items = tree.get_children()
        for item in items:
            node = self.tree_node_to_xml('', item)
            root.append(node)

        # restore filter
        self.filter_restore()

        return ET.ElementTree(root)

    def tree_node_to_xml(self, parent, item):
        """Converts a treeview item and children to xml nodes"""

        tree = self.treeview
        data = self.treedata[item]
        node = data.to_xml_node()

        children = tree.get_children(item)
        for child in children:
            cnode = ET.Element('child')
            cwidget = self.tree_node_to_xml(item, child)
            cnode.append(cwidget)
            node.append(cnode)

        return node

    def _insert_item(self, root, data, from_file=False):
        """Insert a item on the treeview and fills columns from data"""

        tree = self.treeview
        treelabel = data.get_id()
        row = col = ''
        if root != '' and 'layout' in data:
            row = data.get_layout_property('row')
            col = data.get_layout_property('column')

            # fix row position when using copy and paste
            # If collision, increase by 1
            row_count = self.get_max_row(root)
            if not from_file and (row_count > int(row) and int(col) == 0):
                row = str(row_count + 1)
                data.set_layout_property('row', row)

        image = ''
        try:
            image = StockImage.get('16x16-tk.default')
        except StockImageException:
            # TODO: notify something here
            pass

        try:
            image = StockImage.get('16x16-{0}'.format(data.get_class()))
        except StockImageException:
            # TODO: notify something here
            pass

        values = (data.get_class(), row, col)
        item = tree.insert(root, 'end', text=treelabel, values=values,
                           image=image)
        data.attach(self)
        self.treedata[item] = data

        # Update grid r/c data
        self._update_max_grid_rc(root, from_file=True)
        self.app.set_changed()

        return item

    def _update_max_grid_rc(self, item, from_file=False):
        # Calculate max grid row/col for item
        if item != '':
            item_data = self.treedata[item]
            row, col = self.get_max_row_col(item)
            item_data.max_col = col
            item_data.max_row = row
            if not from_file:
                item_data.remove_unused_grid_rc()

    def copy_to_clipboard(self):
        """
        Copies selected items to clipboard.
        """
        tree = self.treeview
        # get the selected item:
        selection = tree.selection()
        if selection:
            self.filter_remove(remember=True)
            root = ET.Element('selection')
            for item in selection:
                node = self.tree_node_to_xml('', item)
                root.append(node)
            # python2 issue
            try:
                text = ET.tostring(root, encoding='unicode')
            except LookupError:
                text = ET.tostring(root, encoding='UTF-8')
            tree.clipboard_clear()
            tree.clipboard_append(text)
            self.filter_restore()

    def cut_to_clipboard(self):
        self.copy_to_clipboard()
        self.on_treeview_delete_selection()

    def _validate_add(self, root_item, classname, show_warnings=True):
        is_valid = True

        new_boclass = builder.CLASS_MAP[classname].builder
        root = root_item
        if root:
            root_classname = self.treedata[root].get_class()
            root_boclass = builder.CLASS_MAP[root_classname].builder
            # print('rootclass:', root_classname)

            allowed_children = root_boclass.allowed_children
            # print('allowed_children:', allowed_children)

            if allowed_children:
                if classname not in allowed_children:
                    str_children = ', '.join(allowed_children)
                    msg = _('Allowed children: {0}.')
                    msg = msg.format(str_children)
                    if show_warnings:
                        logger.warning(msg)
                    is_valid = False
                    return is_valid

            children_count = len(self.treeview.get_children(root))
            maxchildren = root_boclass.maxchildren
#            print('root children:', children_count)
            if maxchildren is not None and children_count >= maxchildren:
                msg = _('Only {0} children allowed for {1}')
                msg = msg.format(maxchildren, root_classname)
                if show_warnings:
                    logger.warning(msg)
                is_valid = False
                return is_valid

            allowed_parents = new_boclass.allowed_parents
            if (allowed_parents is not None and
               root_classname not in allowed_parents):
                msg = _('{0} not allowed as parent of {1}')
                msg = msg.format(root_classname, classname)
                if show_warnings:
                    logger.warning(msg)
                is_valid = False
                return is_valid

            if allowed_children is None and root_boclass.container is False:
                msg = _('Not allowed, {0} is not a container.')
                msg = msg.format(root_classname)
                if show_warnings:
                    logger.warning(msg)
                is_valid = False
                return is_valid

        else:
            # allways show warning when inserting in top level
            # if insertion is at top level,
            # Validate if it can be added at root level
            allowed_parents = new_boclass.allowed_parents
            if allowed_parents is not None and 'root' not in allowed_parents:
                msg = _('{0} not allowed at root level')
                msg = msg.format(classname)
                logger.warning(msg)
                is_valid = False
                return is_valid

            # if parents are not specified as parent,
            # check that item to insert is a container.
            # only containers are allowed at root level
            if new_boclass.container is False:
                msg = _('Not allowed at root level, {0} is not a container.')
                msg = msg.format(classname)
                logger.warning(msg)
                is_valid = False
                return is_valid
        return is_valid

    def _is_unique_id(self, root, widget_id):
        unique = True
        if root != '':
            data = self.treedata[root]
            if data.get_id() == widget_id:
                unique = False
        if unique is True:
            for item in self.treeview.get_children(root):
                unique = self._is_unique_id(item, widget_id)
                if unique is False:
                    break
        return unique

    def _generate_id(self, classname, index, base=None):
        class_base_name = classname.split('.')[-1]
        name = class_base_name
        if base is not None:
            name = base
            if class_base_name in base:
                name = name.split('_')[0]
        name = '{0}_{1}'.format(name, index)
        return name

    def get_unique_id(self, classname, start_id=None):
        if start_id is None:
            self.counter[classname] += 1
            start_id = self._generate_id(classname, self.counter[classname])

        is_unique = self._is_unique_id('', start_id)
        while is_unique is False:
            self.counter[classname] += 1
            start_id = self._generate_id(classname,
                                         self.counter[classname], start_id)
            is_unique = self._is_unique_id('', start_id)

        # print('unique_calculated:', start_id)
        return start_id

    def paste_from_clipboard(self):
        self.filter_remove(remember=True)
        tree = self.treeview
        selected_item = ''
        selection = tree.selection()
        if selection:
            selected_item = selection[0]
        try:
            text = tree.selection_get(selection='CLIPBOARD')
            # python 2 issues
            try:
                root = ET.fromstring(text)
            except UnicodeEncodeError:
                parser = ET.XMLParser(encoding='UTF-8')
                root = ET.XML(text.encode('UTF-8'), parser)
            for element in root:
                data = WidgetDescr(None, None)
                data.from_xml_node(element)
                if self._validate_add(selected_item, data.get_class()):
                    self.populate_tree(selected_item, root, element)
            self.draw_widget(selected_item)
        except ET.ParseError:
            # TODO: show warning here.
            pass
        except tk.TclError:
            pass
        self.filter_restore()

    def add_widget(self, wclass):
        """Adds a new item to the treeview."""

        tree = self.treeview
        #  get the selected item:
        selected_item = ''
        tsel = tree.selection()
        if tsel:
            selected_item = tsel[0]

        #  Need to remove filter if set
        self.filter_remove()

        root = selected_item
        #  check if the widget can be added at selected point
        if not self._validate_add(root, wclass, False):
            #  if not try to add at item parent level
            parent = tree.parent(root)
            if parent != root:
                if self._validate_add(parent, wclass):
                    root = parent
                else:
                    return
            else:
                return

        #  root item should be set at this point
        #  setup properties
        widget_id = self.get_unique_id(wclass)

        data = WidgetDescr(wclass, widget_id)

        # setup default values for properties
        for pname in builder.CLASS_MAP[wclass].builder.properties:
            pdescription = {}
            if pname in properties.WIDGET_PROPERTIES:
                pdescription = properties.WIDGET_PROPERTIES[pname]
            if wclass in pdescription:
                pdescription = dict(pdescription, **pdescription[wclass])
            default_value = str(pdescription.get('default', ''))
            data.set_property(pname, default_value)
            # default text for widgets with text prop:
            if pname in ('text', 'label'):
                data.set_property(pname, widget_id)

        #
        #  default grid properties
        #
        # is_container = builder.CLASS_MAP[wclass].builder.container
        for prop_name in properties.GRID_PROPERTIES:
            pdescription = properties.LAYOUT_OPTIONS[prop_name]
            if wclass in pdescription:
                pdescription = dict(pdescription, **pdescription[wclass])
            default_value = str(pdescription.get('default', ''))
            data.set_layout_property(prop_name, default_value)

        rownum = '0'
        if root:
            rownum = str(self.get_max_row(root)+1)
        data.set_layout_property('row', rownum)
        data.set_layout_property('column', '0')

        item = self._insert_item(root, data)

        # Do redraw
        self.draw_widget(item)

        # Select and show the item created
        tree.after_idle(lambda: tree.selection_set(item))
        tree.after_idle(lambda: tree.focus(item))
        tree.after_idle(lambda: tree.see(item))

    def remove_all(self):
        self.filter_remove()
        children = self.treeview.get_children()
        if children:
            self.treeview.delete(*children)
        self.widget_editor.hide_all()

    def load_file(self, filename):
        """Load file into treeview"""

        self.counter.clear()
        # python2 issues
        try:
            etree = ET.parse(filename)
        except ET.ParseError:
            parser = ET.XMLParser(encoding='UTF-8')
            etree = ET.parse(filename, parser)
        eroot = etree.getroot()

        self.remove_all()
        self.previewer.remove_all()
        self.widget_editor.hide_all()

        self.previewer.resource_paths.append(os.path.dirname(filename))
        for element in eroot:
            self.populate_tree('', eroot, element,from_file=True)
        children = self.treeview.get_children('')
        for child in children:
            self.draw_widget(child)
        self.previewer.show_selected(None, None)

    def populate_tree(self, master, parent, element,from_file=False):
        """Reads xml nodes and populates tree item"""

        data = WidgetDescr(None, None)
        data.from_xml_node(element)
        cname = data.get_class()
        uniqueid = self.get_unique_id(cname, data.get_id())
        data.set_property('id', uniqueid)

        if cname in builder.CLASS_MAP:
            pwidget = self._insert_item(master, data,from_file=from_file)
            xpath = "./child"
            children = element.findall(xpath)
            for child in children:
                child_object = child.find('./object')
                cwidget = self.populate_tree(pwidget, child, child_object,from_file=from_file)

            return pwidget
        else:
            raise Exception('Class "{0}" not mapped'.format(cname))

    def get_max_row(self, item):
        tree = self.treeview
        max_row = -1
        children = tree.get_children(item)
        for child in children:
            data = self.treedata[child].get('layout', {})
            row = int(data.get('row', 0))
            if row > max_row:
                max_row = row
        return max_row

    def on_treeview_select(self, event):
        tree = self.treeview
        sel = tree.selection()
        if sel:
            item = sel[0]
            top = self.get_toplevel_parent(item)
            selected_id = self.treedata[item].get_id()
            self.previewer.show_selected(top, selected_id)
            # max_rc = self.get_max_row_col(item)
            self.widget_editor.edit(self.treedata[item])
        else:
            # No selection hide all
            self.widget_editor.hide_all()

    def get_max_row_col(self, item):
        tree = self.treeview
        max_row = 0
        max_col = 0
        children = tree.get_children(item)
        for child in children:
            data = self.treedata[child]
            row = int(data.get_layout_property('row'))
            col = int(data.get_layout_property('column'))
            if row > max_row:
                max_row = row
            if col > max_col:
                max_col = col
        return (max_row, max_col)

    def update_event(self, hint, obj):
        """Updates tree colums when itemdata is changed."""

        tree = self.treeview
        data = obj
        item = self.get_item_by_data(obj)
        if item:
            if data.get_id() != tree.item(item, 'text'):
                tree.item(item, text=data.get_id())
            # if tree.parent(item) != '' and 'layout' in data:
            if tree.parent(item) != '':
                row = data.get_layout_property('row')
                col = data.get_layout_property('column')
                values = tree.item(item, 'values')
                if (row != values[1] or col != values[2]):
                    values = (data.get_class(), row, col)
                tree.item(item, values=values)
            self.draw_widget(item)
            self.app.set_changed()

    def get_item_by_data(self, data):
        skey = None
        for key, value in self.treedata.items():
            if value == data:
                skey = key
                break
        return skey

    def on_item_move_up(self, event):
        tree = self.treeview
        sel = tree.selection()
        if sel:
            self.filter_remove(remember=True)
            item = sel[0]
            parent = tree.parent(item)
            prev = tree.prev(item)
            if prev:
                prev_idx = tree.index(prev)
                tree.move(item, parent, prev_idx)
            self.filter_restore()

    def on_item_move_down(self, event):
        tree = self.treeview
        sel = tree.selection()
        if sel:
            self.filter_remove(remember=True)
            item = sel[0]
            parent = tree.parent(item)
            next = tree.next(item)
            if next:
                next_idx = tree.index(next)
                tree.move(item, parent, next_idx)
            self.filter_restore()

    #
    # Item grid move functions
    #
    def on_item_grid_move(self, direction):
        tree = self.treeview
        selection = tree.selection()
        if selection:
            self.filter_remove(remember=True)

            for item in selection:
                data = self.treedata[item]

                if direction == self.GRID_UP:
                    row = int(data.get_layout_property('row'))
                    if row > 0:
                        row = row - 1
                        data.set_layout_property('row', str(row))
                        data.notify()
                elif direction == self.GRID_DOWN:
                    row = int(data.get_layout_property('row'))
                    row = row + 1
                    data.set_layout_property('row', str(row))
                    data.notify()
                elif direction == self.GRID_LEFT:
                    column = int(data.get_layout_property('column'))
                    if column > 0:
                        column = column - 1
                        data.set_layout_property('column', str(column))
                        data.notify()
                elif direction == self.GRID_RIGHT:
                    column = int(data.get_layout_property('column'))
                    column = column + 1
                    data.set_layout_property('column', str(column))
                    data.notify()
                root = tree.parent(item)
                self._update_max_grid_rc(root)
            self.filter_restore()

    #
    # Filter functions
    #
    def filter_by(self, string):
        """Filters treeview"""

        self._reatach()
        if string == '':
            self.filter_remove()
            return

        self._expand_all()
        self.treeview.selection_set('')

        children = self.treeview.get_children('')
        for item in children:
            _, detached = self._detach(item)
            if detached:
                self._detached.extend(detached)
        for i, p, idx in self._detached:
            # txt = self.treeview.item(i, 'text')
            self.treeview.detach(i)
        self.filter_on = True

    def filter_remove(self, remember=False):
        if self.filter_on:
            sitem = None
            selection = self.treeview.selection()
            if selection:
                sitem = selection[0]
                self.treeview.after_idle(lambda: self._see(sitem))
            if remember:
                self.filter_prev_value = self.filtervar.get()
                self.filter_prev_sitem = sitem
            self._reatach()
            self.filtervar.set('')
        self.filter_on = False

    def filter_restore(self):
        if self.filter_prev_value:
            self.filtervar.set(self.filter_prev_value)
            item = self.filter_prev_sitem
            if item and self.treeview.exists(item):
                self.treeview.selection_set(item)
                self.treeview.after_idle(lambda: self._see(item))
            # clear
            self.filter_prev_value = ''
            self.filter_prev_sitem = None

    def _see(self, item):
        # The item may have been deleted.
        try:
            self.treeview.see(item)
        except tk.TclError:
            pass

    def _expand_all(self, rootitem=''):
        children = self.treeview.get_children(rootitem)
        for item in children:
            self._expand_all(item)
        if rootitem != '' and children:
            self.treeview.item(rootitem, open=True)

    def _reatach(self):
        """Reinsert the hidden items."""
        for item, p, idx in self._detached:
            # The item may have been deleted.
            if self.treeview.exists(item) and self.treeview.exists(p):
                self.treeview.move(item, p, idx)
        self._detached = []

    def _detach(self, item):
        """Hide items from treeview that do not match the search string."""
        to_detach = []
        children_det = []
        children_match = False
        match_found = False

        value = self.filtervar.get()
        txt = self.treeview.item(item, 'text').lower()
        if value in txt:
            match_found = True
        else:
            class_txt = self.treedata[item].get_class().lower()
            if value in class_txt:
                match_found = True

        parent = self.treeview.parent(item)
        idx = self.treeview.index(item)
        children = self.treeview.get_children(item)
        if children:
            for child in children:
                match, detach = self._detach(child)
                children_match = children_match | match
                if detach:
                    children_det.extend(detach)

        if match_found:
            if children_det:
                to_detach.extend(children_det)
        else:
            if children_match:
                if children_det:
                    to_detach.extend(children_det)
            else:
                to_detach.append((item, parent, idx))
        match_found = match_found | children_match
        return match_found, to_detach

    #
    # End Filter functions
    #
