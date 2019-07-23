[![Build Status](https://travis-ci.org/alejandroautalan/pygubu.svg?branch=master)](https://travis-ci.org/alejandroautalan/pygubu)

Bienvenue
============================================

`Pygubu` est un [logiciel RAD](https://fr.wikipedia.org/wiki/D%C3%A9veloppement_rapide_d%27applications) pour développer _rapidement_ et _facilement des interfaces utilisateur_ avec le module `tkinter` en Python.

Les interfaces utilisateur conçues sont sauvées au format [XML](https://fr.wikipedia.org/wiki/Extensible_Markup_Language), et grâce à l'utilisation du _constructeur pygubu_, elles peuvent être chargées dynamiquement par les applications, si nécessaire.

Pygubu est inspiré de [Glade](https://glade.gnome.org).

Installation
====

Pygubu requiert Python >= 2.7 (Testé seulement avec Python 2.7.3, 3.2.3 avec tk8.5).

Vous pouvez installer pygubu par :

### l'archive zip

Téléchargez et décompressez l'archive. Ouvrez un terminal, dirigez-vous vers le répertoire d'extraction puis exécutez :

```
python setup.py install
```

### pip

```
pip install pygubu
```

Notez que si vous utilisez Python 3, vous pouvez utiliser son propre outil `pip`, par exemple :

    pip3.5 install pygubu

Dans le cas précédent, j'utilise l'outil `pip` de Python 3.5

Pour vérifier le succès de l'installation, vous pouvez essayer d'importer `pygubu` - par exemple depuis [IDLE](https://fr.wikipedia.org/wiki/IDLE_(Python))

    import pygubu
    
Si vous n'avez pas d'erreur [`ImportError`](https://docs.python.org/3.5/library/exceptions.html#ImportError), alors votre installation s'est faite avec succès.

Utilisation
=====

Écrivez dans un terminal la commande suivante, selon votre système

### Unix-like systems

```
pygubu-designer
```
Si vous avez une erreur du type "No module named 'appdirs'", vous pouvez mettre à jour par
```
wget https://pypi.python.org/packages/48/69/d87c60746b393309ca30761f8e2b49473d43450b150cb08f3c6df5c11be5/appdirs-1.4.3.tar.gz
gunzip appdirs-1.4.3.tar.gz
tar -xvf appdirs-1.4.3.tar
cd appdirs-1.4.3
sudo python setup.py install
```


### Windows

```
C:\Python34\Scripts\pygubu-designer.exe
```

Où `C:\Python34`  est le chemin de **votre** répertoire d'installation de Python.

> **Note** : pour les versions antérieures à **0.9.8**, l'exécutable était nommé _**pygubu-designer.bat**_

Ensuite, l'application _pygubu-designer_ devrait apparaître, telle quelle :

<img src="pygubu-designer.png" alt="pygubu-desinger.png">


Maintenant, vous pouvez commancer à créer votre application tkinter en utilisant les widgets que vous trouverez dans le panneau de gauche, appelé `Widget List`.

Après que vous ayez terminé de créer votre _interface UI_, sauvegardez-la en tant que fichier `.ui`  par l'usage du menu `File > Save`.

Ce qui suit est un exemple d'interface UI, appelé [helloworld.ui](examples/helloworld.ui), créé en utilisant pygubu : 


```xml
<?xml version='1.0' encoding='utf-8'?>
<interface>
  <object class="ttk.Frame" id="mainwindow">
    <property name="height">200</property>
    <property name="padding">20</property>
    <property name="width">200</property>
    <layout>
      <property name="column">0</property>
      <property name="propagate">True</property>
      <property name="row">0</property>
      <property name="sticky">nesw</property>
    </layout>
    <child>
      <object class="ttk.Label" id="label1">
        <property name="anchor">center</property>
        <property name="font">Helvetica 26</property>
        <property name="foreground">#0000b8</property>
        <property name="text" translatable="yes">Hello World !</property>
        <layout>
          <property name="column">0</property>
          <property name="propagate">True</property>
          <property name="row">0</property>
        </layout>
      </object>
    </child>
  </object>
  </interface>
```

Ensuite, vous devez créer votre _script d'application_, tel que ci-dessous :


```python
#test.py
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu


class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('helloworld.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', master)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
```

Notez l'ajout de `helloworld.ui` dans la ligne suivante :

```python
builder.add_from_file('helloworld.ui')
```

Vous devez insérer le _nom du fichier_ (ou son chemin). 

Notez aussi l'ajout de `'mainwindow'` dans la ligne suivante : 

```python
self.mainwindow = builder.get_object('mainwindow', master)
```

Vous devez avoir le nom de votre _widget main_ (le parent de tous les widgets), sinon vous obtiendrez l'erreur similaire : 
    
    Exception: Widget not defined.

See [this](https://github.com/alejandroautalan/pygubu/issues/40) issue for more information.



Documentation
=============

Visitez le [wiki](https://github.com/alejandroautalan/pygubu/wiki) pygubu pour consulter la documentation.


Voici quelques bonnes références de tkinter (et tk) :

- [TkDocs](http://www.tkdocs.com)
- [Graphical User Interfaces with Tk](http://docs.python.org/3.5/library/tk.html)
- [Tkinter 8.5 reference: a GUI for Python](https://web.archive.org/web/20181211092656/http://infohost.nmt.edu/~shipman/soft/tkinter/web/index.html)
- [An Introduction to Tkinter](http://effbot.org/tkinterbook/)
- [Tcl/Tk 8.5 Manual](http://www.tcl.tk/man/tcl8.5/)


Vous pouvez aussi voir le répertoire [examples](examples) ou regarder [ce tutoriel d'introduction en vidéo](http://youtu.be/wuzV9P8geDg).


Histoire
=======

Consultez la liste des changements [ici](HISTORY.md).


