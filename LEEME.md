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

Descarga y descomprime el paquete fuente. Abre una consola en el directorio de
extracción y ejecuta:

```
python setup.py install
```


Modo de uso
===========

Crea una interfaz de usuario usando pygubu y guárdala en un archivo (ejemplo: prueba.ui). Luego, crea tu aplicación como se muestra a continuación:

```python
#prueba.py
import tkinter as tk
import pygubu

class Application:
    def __init__(self, master):

        #1: Crea un constructor
        self.builder = builder = pugubu.Builder()

        #2: Carga un archivo con el diseño de la interfaz
        builder.add_from_file('prueba.ui')

        #3: Crea el widget usando 'master' como padre
        self.mainwindow = builder.get_object('mainwindow', master)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
```

Busca en el directorio de ejemplos o mira este ejemplo de 'Hola mundo' en
vídeo http://youtu.be/wuzV9P8geDg


Historia
========

Cambios de la versión 0.8

  * Added translation support
  * Translated pygubu designer to Spanish

Cambios de la versión 0.7

  * Added python 2.7 support
  * Added initial TkApplication class
  * Fixed some bugs.

Primera versión pública 0.6
