History
=======

Changes for version 0.9.8

  * Use entry_points field for installing a startup script with setuptools
  * Fixed issues #66, #86
  
Changes for version 0.9.7.9

  * Fixed issues #72, #74, #78, #81

Changes for version 0.9.7.8

  * Added wheel support.
  * Fixed issues #64, #65

Changes for version 0.9.7.7

  * Improved ui tester.
  * Fixed issues #54, #58, #59, #60

Changes for version 0.9.7.5

  * Allow to specify variable names when importing tk variables.
  * Allow to register an already created tk image.
  * Allow to specify loggin level from console command.
  * Added new pathchooser input widget.
  * Improved README (thanks to Nelson Brochado)
  * Fixed issue #52

Changes for version 0.9.7.3

  * Added custom widgets preference option.
  * Added appdirs dependency.
  * New sticky property editor.
  * Fixed issues #40, #45

Changes for version 0.9.7

  * Fixed issues #39, #41 

Changes for version 0.9.6.7

  * Remove old pygubu.py script for old installations.
    Create pybugu-designer.bat file for windows platform. Fixes #38

Changes for version 0.9.6.6

  * Fixed bug: color value setting to None when presing Cancel on color selector.
  * Add '.png' format to Stockimage if tk version support it. fixes #36
  * Minor changes to main UI.

Changes for version 0.9.6.5

  * Fixed bug on menu creation.
  * Fixed issues #14 and #22
  * Added helper method to avoid call get_variable for every variable. refs #29

Changes for version 0.9.6.4

  * Fixed bug #33 "Wrong textvariable format when create ui file"

Changes for version 0.9.6.3

  * Use old menu preview on platforms other than linux  (new preview does not work on windows)

Changes for version 0.9.6.2

  * Property editors rewritten from scratch
  * Improved menu preview
  * Added font property editor
  * Fixed menu issues

Changes for version 0.9.5.1

  * Add select hotkey to widget tree. (i - select previous item, k - select next item)
  * Copied menu example from wiki to examples folder.

Changes for version 0.9.5

  * Renamed designer startup script to pygubu-designer (see [#20](/../../issues/20))
  * Fixed bugs.

Changes for version 0.9.4

  * Added Toplevel widget
  * Added generic Dialog widget
  * Rewrited scrolledframe widget internals, ideas and code taken from tkinter wiki.
  * Added more widget icons.
  * Fixed bugs.

Changes for version 0.9.3
    
  * Allow to select control variable type
  * Fixed some bugs.

Changes for version 0.9.2

  * Added more wiki pages.
  * Fixed issues #3, #4

Changes for version 0.9.1

  * Separate designer module from main package
  * Added menu to select current ttk theme
  * Fix color selector issues.

Changes for version 0.9

  * Add validator for pax and pady properties.
  * Improved ScrolledFrame widget.
  * Added more wiget icons.
  * Fix cursor type on preview panel.

Changes for version 0.8

  * Added translation support
  * Translated pygubu designer to Spanish

Changes for version 0.7

  * Added python 2.7 support
  * Added initial TkApplication class
  * Fixed some bugs.

First public version 0.6
