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
from pygubudesigner.widgets.propertyeditor import *


class DynamicPropertyEditor(PropertyEditor):

    def _create_ui(self):
        self._current = None
        self._editors = {}
        self._indexes = {}
        self._last_idx = -1
        self._current = self._create_editor('entry')
        self.columnconfigure(0, weight=1)

    def _create_editor(self, mode):
        editor = e = create_editor(mode, self)
        self._last_idx += 1
        e.grid(row=self._last_idx, column=0, sticky='we')
        self._editors[mode] = editor
        self._indexes[mode] = self._last_idx
        editor.bind('<<PropertyChanged>>', self._on_variable_changed)
        return editor

    def _get_value(self):
        return self._current.value

    def _set_value(self, value):
        self._current.edit(value)

    def parameters(self, **kw):
        modes = kw.pop('modes', None)
        if modes is not None:
            self._configure_modes(modes)
        current = kw.pop('mode', 'entry')
        self.set_mode(current)
        self._current.parameters(**kw)

    def _configure_modes(self, modes):
        for mode in modes:
            if mode not in self._editors:
                self._create_editor(mode)

    def set_mode(self, mode):
        if mode not in self._editors:
            self._create_editor(mode)
        for name, widget in self._editors.items():
            if mode == name:
                widget.grid()
            else:
                widget.grid_remove()
        self._current = self._editors[mode]

register_editor('dynamic', DynamicPropertyEditor)
