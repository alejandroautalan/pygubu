#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import subprocess
import shlex

gtk_imgs = {
    'widget-gtk-button.png': ('ttk.Button', 'tk.Button'),
    'widget-gtk-calendar.png': ('tk.Calendar', 'pygubu.builder.widgets.calendarframe'),
    'widget-gtk-checkbutton.png': ('tk.Checkbutton', 'ttk.Checkbutton'),
    'widget-gtk-checkmenuitem.png': ('tk.Menuitem.Checkbutton',),
    'widget-gtk-combobox.png': ('ttk.Combobox', 'pygubu.builder.widgets.combobox'),
    'widget-gtk-default.png': ('tk.default',),
    'widget-gtk-drawingarea.png': ('tk.Canvas',),
    'widget-gtk-entry.png': ('tk.Entry', 'ttk.Entry', 'pygubu.builder.widgets.pathchooserinput'),
    'widget-gtk-frame.png': ('tk.Frame', 'ttk.Frame'),
    'widget-gtk-hscale.png': ('tk.Scale', 'ttk.Scale'),
    'widget-gtk-hscrollbar.png': ('tk.Scrollbar', 'ttk.Scrollbar'),
    'widget-gtk-image.png': tuple(),
    'widget-gtk-label.png': ('tk.Label', 'ttk.Label'),
    'widget-gtk-menubar.png': tuple(),
    'widget-gtk-menuitem.png': ('tk.Menuitem.Command',),
    'widget-gtk-menu.png': ('tk.Menu', 'tk.Menuitem.Submenu'),
    'widget-gtk-menutoolbutton.png': ('tk.Menubutton', 'ttk.Menubutton'),
    'widget-gtk-notebook.png': ('ttk.Notebook',),
    'widget-gtk-paned.png': ('tk.PanedWindow', 'ttk.Panedwindow',
            'tk.PanedWindow.Pane', 'ttk.Panedwindow.Pane'),
    'widget-gtk-progressbar.png': ('ttk.Progressbar',),
    'widget-gtk-radiobutton.png': ('tk.Radiobutton', 'ttk.Radiobutton'),
    'widget-gtk-radiomenuitem.png': ('tk.Menuitem.Radiobutton',),
    'widget-gtk-scale.png': tuple(),
    'widget-gtk-scrolledwindow.png': ('pygubu.builder.widgets.scrolledframe',
            'pygubu.builder.widgets.tkscrolledframe'),
    'widget-gtk-separatormenuitem.png': ('tk.Menuitem.Separator',),
    'widget-gtk-separator.png': ('ttk.Separator',),
    'widget-gtk-spinbutton.png': ('tk.Spinbox', 'ttk.Spinbox'),
    'widget-gtk-textview.png': ('tk.Text',),
    'widget-gtk-treeview.png': ('tk.Listbox', 'ttk.Treeview',
        'pygubu.builder.widgets.editabletreeview'),
    'widget-gtk-viewport.png': ('pygubu.builder.widgets.scrollbarhelper',
            'pygubu.builder.widgets.tkscrollbarhelper'),
    'widget-gtk-window.png': ('tk.Toplevel', 'pygubu.builder.widgets.dialog'),
}

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'pygubudesigner', 'images', 'widgets')


def create_images():
    origin = os.path.join(IMG_DIR, 'png', '22x22')
    dest = os.path.join(IMG_DIR, '22x22')

    for f, v in gtk_imgs.items():
        iimage = os.path.join(origin, f)
        for output in v:
            print('.', end='', flush=True)
            oimage = os.path.join(dest, output)
            cmd = 'convert {0} {1}.gif'.format(iimage, oimage)
            cmd = shlex.split(cmd)
            subprocess.call(cmd)

    print('\n16x16')
    origin = os.path.join(IMG_DIR, '22x22')
    dest = os.path.join(IMG_DIR, '16x16')
    for f in os.listdir(origin):
        print('.', end='', flush=True)
        iimage = os.path.join(origin, f)
        oimage = os.path.join(dest, f)
        cmd = 'convert {0} -filter Hermite -format gif ' \
            '-background transparent -bordercolor white -border 0x0 ' \
            '-resize 16 {1}'.format(iimage, oimage)
        cmd = shlex.split(cmd)
        subprocess.call(cmd)
    print('')


def find_source_image_for(widget_name):
    found = None
    for k, v in gtk_imgs.items():
        if widget_name in v:
            found = k
            break
    return found


def create_image_for(widget_name):
    origin = os.path.join(IMG_DIR, 'png', '22x22')
    dest = os.path.join(IMG_DIR, '22x22')

    source = find_source_image_for(widget_name)
    if source:
        iimage = os.path.join(origin, source)
        oimage = os.path.join(dest, widget_name)
        cmd = 'convert {0} {1}.gif'.format(iimage, oimage)
        cmd = shlex.split(cmd)
        subprocess.call(cmd)

        origin = os.path.join(IMG_DIR, 'png', '22x22')
        dest = os.path.join(IMG_DIR, '16x16')
        iimage = os.path.join(origin, source)
        oimage = os.path.join(dest, widget_name)
        cmd = 'convert {0} -filter Hermite -format gif ' \
              '-background transparent -bordercolor white -border 0x0 ' \
              '-resize 16 {1}.gif'.format(iimage, oimage)
        cmd = shlex.split(cmd)
        subprocess.call(cmd)
    else:
        print('Widget not defined :(')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == 'all':
            create_images()
        else:
            create_image_for(arg)
    else:
        print('Usage: create-imgs [all, widget_name]')
