Bienvenido a pygubu un diseñador de interfaces para tkinter.
============================================

Pygubu es una herramienta RAD que permite desarrollar interfaces de usuario
rápida y fácilmente para el modulo tkinter de python.

La interfaces diseñadas se guardan como archivos XML, y usando el constructor
de pygubu estos pueden ser cargados dinámicamente por las aplicaciones
a medida que lo necesiten
Pygubu esta inspirado por Glade (el diseñador de interfaces de gtk).

Instalación
============

Pygubu requiere python >= 2.7 (Probado solo en python 2.7.3 y 3.2.3 con tk8.5)

Usando paquete zip:

Descarga y descomprime el paquete fuente. Abre una consola en el directorio de
extracción y ejecuta:

```
python setup.py install
```

Usando pip:

```
pip install pygubu
```

Modo de uso
===========

Crea una interfaz de usuario usando pygubu y guárdala en un archivo (ejemplo: holamundo.ui).

[holamundo.ui] (examples/helloworld.ui)

Luego, crea tu aplicación como se muestra a continuación:

```python
#prueba.py
import tkinter as tk
import pygubu


class Application:
    def __init__(self, master):

        #1: Crea un constructor
        self.builder = builder = pygubu.Builder()

        #2: Carga un archivo con el diseño de la interfaz
        builder.add_from_file('holamundo.ui')

        #3: Crea el widget usando 'master' como padre
        self.mainwindow = builder.get_object('mainwindow', master)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
```


Documentación
=============

Visita la [wiki](https://github.com/alejandroautalan/pygubu/wiki) para mas documentación.

Una excelente referencia sobre tkinter esta disponible [aqui](http://www.nmt.edu/tcc/help/pubs/tkinter/web/index.html) (en inglés).

Busca en el directorio de ejemplos o mira este ejemplo de 'Hola mundo' en
[vídeo](http://youtu.be/wuzV9P8geDg)


Historia
========

Cambios de la versión 0.9.6.4

  * Fixed bug #33 "Wrong textvariable format when create ui file"

Cambios de la versión 0.9.6.3

  * Use old menu preview on platforms other than linux  (new preview does not work on windows)

Cambios de la versión 0.9.6.2

  * Property editors rewritten from scratch
  * Improved menu preview
  * Added font property editor
  * Fixed menu issues

Cambios de la versión 0.9.5.1

  * Add select hotkey to widget tree. (i - select previous item, k - select next item)
  * Copied menu example from wiki to examples folder.

Cambios de la versión 0.9.5

  * Renamed designer startup script to pygubu-designer (ver [#20](/../../issues/20))
  * Fixed bugs.

Cambios de la versión 0.9.4

  * Added Toplevel widget
  * Added generic Dialog widget
  * Rewrited scrolledframe widget internals, ideas and code taken from tkinter wiki.
  * Added more widget icons.
  * Fixed bugs.

Cambios de la versión 0.9.3
    
    * Allow to select control variable type
    * Fixed some bugs.

Cambios de la versión 0.9.2

  * Added more wiki pages.
  * Fixed issues #3, #4

Cambios de la versión 0.9.1

  * Separate designer module from main package
  * Added menu to select current ttk theme
  * Fix color selector issues.

Cambios de la versión 0.9

  * Add validator for pax and pady properties.
  * Improved ScrolledFrame widget.
  * Added more wiget icons.
  * Fix cursor type on preview panel.

Cambios de la versión 0.8

  * Added translation support
  * Translated pygubu designer to Spanish

Cambios de la versión 0.7

  * Added python 2.7 support
  * Added initial TkApplication class
  * Fixed some bugs.

Primera versión pública 0.6
