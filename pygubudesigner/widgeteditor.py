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
#
# For further info, check  http://pygubu.web.here
from __future__ import unicode_literals, print_function

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubu import builder
from pygubudesigner.propertieseditor import PropertiesEditor
from pygubudesigner.bindingseditor import BindingsEditor
from pygubudesigner.layouteditor import LayoutEditor


class WidgetEditor(object):

    def __init__(self, propsframe, layoutframe, bindingstree):
        self.properties_editor = PropertiesEditor(propsframe)
        self.layout_editor = LayoutEditor(layoutframe)
        self.bindings_editor = BindingsEditor(bindingstree)

    def edit(self, wdescr):
        self.properties_editor.edit(wdescr)
        self.layout_editor.edit(wdescr)
        self.bindings_editor.edit(wdescr)

    def hide_all(self):
        self.properties_editor.hide_all()
        self.layout_editor.hide_all()
        self.bindings_editor.hide_all()
