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

from __future__ import unicode_literals
try:
    import tkinter as tk
except:
    import Tkinter as tk


class SelectTool(object):
    def __init__(self, canvas):
        self._canvas = canvas
        self._canvas.region_selected = None
        #variables para el manejo de seleccion
        self._selecting = False
        self._sobject = None
        self._sstart = None

    def click_handler(self, event):
        canvas = self._canvas
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)

        self._start_selecting(event)

    def motion_handler(self, event):
        if self._selecting:
            self._keep_selecting(event)
        
    def release_handler(self, event):
        if self._selecting:
            self._keep_selecting(event)
            self._finish_selecting(event)

    def _start_selecting(self, event):
        """Comienza con el proceso de seleccion."""
        self._selecting = True
        canvas = self._canvas
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        self._sstart = (x, y)
        if not self._sobject:
            self._sobject = canvas.create_rectangle(
                self._sstart[0], self._sstart[1], x, y,
                dash=(3,5), outline='#0000ff'
            )
        canvas.itemconfigure(self._sobject, state=tk.NORMAL)

    def _keep_selecting(self, event):
        """Continua con el proceso de seleccion.
        Crea o redimensiona el cuadro de seleccion de acuerdo con
        la posicion del raton."""
        canvas = self._canvas
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        canvas.coords(self._sobject,
                      self._sstart[0], self._sstart[1], x, y)

    def _finish_selecting(self, event):
        """Finaliza la seleccion.
        Marca como seleccionados todos los objetos que se encuentran
        dentro del recuadro de seleccion."""
        self._selecting = False
        canvas = self._canvas
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        
        canvas.coords(self._sobject, -1, -1, -1, -1)
        canvas.itemconfigure(self._sobject, state=tk.HIDDEN)

        sel_region = self._sstart[0], self._sstart[1], x, y
        canvas.region_selected = sel_region
        canvas.event_generate('<<RegionSelected>>')

