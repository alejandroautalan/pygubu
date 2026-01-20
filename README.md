[Leer en Español](LEEME.md)

Welcome to Pygubu!
==================

`Pygubu` is a [RAD tool](https://en.wikipedia.org/wiki/Rapid_application_development) to enable _quick_ and _easy development of user interfaces_ for the Python's `tkinter` module.

The user interfaces designed are saved as [XML](https://en.wikipedia.org/wiki/XML) files, and, by using the _pygubu builder_, these can be loaded by applications dynamically as needed.

Pygubu is inspired by [Glade](https://gitlab.gnome.org/GNOME/glade).

Installation
============

The latest version of pygubu requires Python >= 3.9

You can install pygubu using pip:

```
pip install pygubu
```

Usage
=====

Since version 0.10 the project was splitted in two main modules:

- The **pygubu core** (this project), that load and build user interfaces defined in xml.
- The **interface editor** [pygubu-designer](https://github.com/alejandroautalan/pygubu-designer), that helps you create the xml definition graphically.

The core also includes:

- A widget set: Pygubu widgets
- Themes: Pygubu bootstrap themes, a set of themes based on ttkbootstrap but
implemented only with tkinter.
- And many helper clases that you can use to build your application.

Pygubu widgets:

- AccordionFrame
- AutoArrangeFrame
- CalendarFrame
- HideableFrame
- ScrolledFrame
- ColorInput
- Combobox
- Dialog
- EditableTreeview
- FilterableTreeview
- FontInput
- PathChooserInput
- PathChooserButton
- Tooltip
- Tooltipttk
- DockFrame
- DockPane
- DockWidget
- Pygubu Forms

Pygubu also has plugins to support working with external widget sets like:

- ttkwidgets
- customtkinter
- awesometkinter
- tkcalendar
- tkintermapview
- tkintertable
- tkinterweb
- TkinterModernThemes
- tksheet.

To start creating your application, please go directly to the [pygubu-designer](https://github.com/alejandroautalan/pygubu-designer) documentation.


Documentation
=============

Visit the [pygubu-designer](https://github.com/alejandroautalan/pygubu-designer) page or the [wiki](https://github.com/alejandroautalan/pygubu-designer/wiki) for more information.


History
=======

See the list of changes [here](HISTORY.md).
