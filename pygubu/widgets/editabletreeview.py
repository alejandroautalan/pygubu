# encoding: utf8
from __future__ import unicode_literals
import functools

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


class EditableTreeview(ttk.Treeview):
    """A simple editable treeview

    It uses the following events from Treeview:
        <<TreviewSelect>>
        <4>
        <5>
        <KeyRelease>
        <Home>
        <End>
        <Configure>
        <Button-1>
        <ButtonRelease-1>
        <Motion>
    If you need them use add=True when calling bind method.

    It Generates two virtual events:
        <<TreeviewInplaceEdit>>
        <<TreeviewCellEdited>>
    The first is used to configure cell editors.
    The second is called after a cell was changed.
    You can know wich cell is being configured or edited, using:
        get_event_info()
    """
    def __init__(self, master=None, **kw):
        ttk.Treeview.__init__(self, master, **kw)

        self._curfocus = None
        self._inplace_widgets = {}
        self._inplace_widgets_show = {}
        self._inplace_vars = {}
        self._header_clicked = False
        self._header_dragged = False

        self.bind('<<TreeviewSelect>>', self.__check_focus)
        #Wheel events?
        self.bind('<4>', lambda e: self.after_idle(self.__updateWnds))
        self.bind('<5>', lambda e: self.after_idle(self.__updateWnds))
        #self.bind('<ButtonRelease-1>', self.__check_focus)
        self.bind('<KeyRelease>', self.__check_focus)
        self.bind('<Home>', functools.partial(self.__on_key_press, 'Home'))
        self.bind('<End>', functools.partial(self.__on_key_press, 'End'))
        self.bind('<Button-1>', self.__on_button1)
        self.bind('<ButtonRelease-1>', self.__on_button1_release)
        self.bind('<Motion>', self.__on_mouse_motion)
        self.bind('<Configure>',
            lambda e: self.after_idle(self.__updateWnds))


    def __on_button1(self, event):
        r = event.widget.identify_region(event.x, event.y)
        if r in ('separator', 'header'):
            self._header_clicked = True

    def __on_mouse_motion(self, event):
        if self._header_clicked:
            self._header_dragged = True

    def __on_button1_release(self, event):
        if self._header_dragged:
            self.after_idle(self.__updateWnds)
        self._header_clicked = False
        self._header_dragged = False

    def __on_key_press(self, key, event):
        if key == 'Home':
            self.selection_set("")
            self.focus(self.get_children()[0])
        if key == 'End':
            self.selection_set("")
            self.focus(self.get_children()[-1])

    def delete(self, *items):
        self.after_idle(self.__updateWnds)
        ttk.Treeview.delete(self, *items)

    def yview(self, *args):
        """Update inplace widgets position when doing vertical scroll"""
        self.after_idle(self.__updateWnds)
        ttk.Treeview.yview(self, *args)

    def yview_scroll(self, number, what):
        self.after_idle(self.__updateWnds)
        ttk.Treeview.yview_scroll(self, number, what)

    def yview_moveto(self, fraction):
        self.after_idle(self.__updateWnds)
        ttk.Treeview.yview_moveto(self, fraction)

    def xview(self, *args):
        """Update inplace widgets position when doing horizontal scroll"""
        self.after_idle(self.__updateWnds)
        ttk.Treeview.xview(self, *args)

    def xview_scroll(self, number, what):
        self.after_idle(self.__updateWnds)
        ttk.Treeview.xview_scroll(self, number, what)

    def xview_moveto(self, fraction):
        self.after_idle(self.__updateWnds)
        ttk.Treeview.xview_moveto(self, fraction)

    def __check_focus(self, event):
        """Checks if the focus has changed"""
        #print('Event:', event.type, event.x, event.y)
        changed = False
        if not self._curfocus:
            changed = True
        elif self._curfocus != self.focus():
            self.__clear_inplace_widgets()
            changed = True
        newfocus = self.focus()
        if changed:
            if newfocus:
                #print('Focus changed to:', newfocus)
                self._curfocus= newfocus
                self.__focus(newfocus)
            self.__updateWnds()

    def __focus(self, item):
        """Called when focus item has changed"""
        cols = self.__get_display_columns()
        for col in cols:
            self.__event_info =(col,item)
            self.event_generate('<<TreeviewInplaceEdit>>')
            if col in self._inplace_widgets:
                w = self._inplace_widgets[col]
                w.bind('<Key-Tab>',
                    lambda e: w.tk_focusNext().focus_set())
                w.bind('<Shift-Key-Tab>',
                    lambda e: w.tk_focusPrev().focus_set())

    def __updateWnds(self, event=None):
        if not self._curfocus:
            return
        item = self._curfocus
        cols = self.__get_display_columns()
        for col in cols:
            if col in self._inplace_widgets:
                wnd = self._inplace_widgets[col]
                bbox = ''
                if self.exists(item):
                    bbox = self.bbox(item, column=col)
                if bbox == '':
                    wnd.place_forget()
                elif col in self._inplace_widgets_show:
                    wnd.place(x=bbox[0], y=bbox[1],
                        width=bbox[2], height=bbox[3])

    def __clear_inplace_widgets(self):
        """Remove all inplace edit widgets."""
        cols = self.__get_display_columns()
        #print('Clear:', cols)
        for c in cols:
            if c in self._inplace_widgets:
                widget = self._inplace_widgets[c]
                widget.place_forget()
                self._inplace_widgets_show.pop(c, None)
                #widget.destroy()
                #del self._inplace_widgets[c]

    def __get_display_columns(self):
        cols = self.cget('displaycolumns')
        show = (str(s) for s in self.cget('show'))
        if '#all' in cols:
            cols = self.cget('columns') + ('#0',)
        elif 'tree' in show:
            cols = cols + ('#0',)
        return cols

    def get_event_info(self):
        return self.__event_info;

    def __get_value(self, col, item):
        if col == '#0':
            return self.item(item, 'text')
        else:
            return self.set(item, col)

    def __set_value(self, col, item, value):
        if col == '#0':
            self.item(item, text=value)
        else:
            self.set(item, col, value)
        self.__event_info =(col,item)
        self.event_generate('<<TreeviewCellEdited>>')

    def __update_value(self, col, item):
        if not self.exists(item):
            return
        value = self.__get_value(col, item)
        newvalue = self._inplace_vars[col].get()
        if value != newvalue:
            self.__set_value(col, item, newvalue)


    def inplace_entry(self, col, item):
        if col not in self._inplace_vars:
            self._inplace_vars[col] = tk.StringVar()
        svar = self._inplace_vars[col]
        svar.set(self.__get_value(col, item))
        if col not in self._inplace_widgets:
            self._inplace_widgets[col] = ttk.Entry(self, textvariable=svar)
        entry = self._inplace_widgets[col]
        entry.bind('<Unmap>', lambda e: self.__update_value(col, item))
        entry.bind('<FocusOut>', lambda e: self.__update_value(col, item))
        self._inplace_widgets_show[col] = True

    def inplace_checkbutton(self, col, item, onvalue='True', offvalue='False'):
        if col not in self._inplace_vars:
            self._inplace_vars[col] = tk.StringVar()
        svar = self._inplace_vars[col]
        svar.set(self.__get_value(col, item))
        if col not in self._inplace_widgets:
            self._inplace_widgets[col] = ttk.Checkbutton(self,
            textvariable=svar, variable=svar, onvalue=onvalue, offvalue=offvalue)
        cb = self._inplace_widgets[col]
        cb.bind('<Unmap>', lambda e: self.__update_value(col, item))
        cb.bind('<FocusOut>', lambda e: self.__update_value(col, item))
        self._inplace_widgets_show[col] = True

    def inplace_combobox(self, col, item, values, readonly=True,
                         update_values=False):
        state = 'readonly' if readonly else 'normal'
        if col not in self._inplace_vars:
            self._inplace_vars[col] = tk.StringVar()
        svar = self._inplace_vars[col]
        svar.set(self.__get_value(col, item))
        if col not in self._inplace_widgets:
            self._inplace_widgets[col] = ttk.Combobox(self,
                textvariable=svar, values=values, state=state)
        if update_values:
            self._inplace_widgets[col].configure(values=values)
        cb = self._inplace_widgets[col]
        cb.bind('<Unmap>', lambda e: self.__update_value(col, item))
        cb.bind('<FocusOut>', lambda e: self.__update_value(col, item))
        self._inplace_widgets_show[col] = True

    def inplace_spinbox(self, col, item, min, max, step):
        if col not in self._inplace_vars:
            self._inplace_vars[col] = tk.StringVar()
        svar = self._inplace_vars[col]
        svar.set(self.__get_value(col, item))
        if col not in self._inplace_widgets:
            self._inplace_widgets[col] = tk.Spinbox(self,
                textvariable=svar, from_=min, to=max, increment=step)
        sb = self._inplace_widgets[col]
        sb.bind('<Unmap>', lambda e: self.__update_value(col, item))
        sb.bind('<FocusOut>', lambda e: self.__update_value(col, item))
        self._inplace_widgets_show[col] = True


    def inplace_custom(self, col, item, widget, stringvar=None):
        if col not in self._inplace_vars:
            if stringvar is None:
                self._inplace_vars[col] = tk.StringVar()
            else:
                self._inplace_vars[col] = stringvar
        svar = self._inplace_vars[col]
        svar.set(self.__get_value(col, item))
        self._inplace_widgets[col] = widget
        widget.bind('<Unmap>', lambda e: self.__update_value(col, item))
        widget.bind('<FocusOut>', lambda e: self.__update_value(col, item))
        self._inplace_widgets_show[col] = True

