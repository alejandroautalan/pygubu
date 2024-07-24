#!/usr/bin/python3
import tkinter as tk
import tkinter.colorchooser
import tkinter.ttk as ttk
from pygubu.utils.widget import WidgetConfigureMixin
from pygubu.widgets.colorinputui import ColorInputUI


#
# Manual user code
#


class ColorInput(WidgetConfigureMixin, ColorInputUI):
    BGCOLOR = ""
    EVENT_COLOR_CHANGED = "<<ColorInput:ColorChanged>>"
    KEY_PRESS_MS = 850

    def __init__(self, master=None, **kw):
        entry_var = kw.pop("textvariable", None)
        super().__init__(master, **kw)
        entry_var = tk.StringVar(value="") if entry_var is None else entry_var
        self._entry_var = entry_var
        self._entry.configure(textvariable=self._entry_var)
        self._color = ""
        self._kp_cb = None

        style = ttk.Style(master)
        cls = type(self)
        cls.BGCOLOR = style.lookup("TFrame", "background")

    def _widget_cget(self, option):
        if option == "value":
            return self._color
        if option == "textvariable":
            return self._entry_var
        return super()._widget_cget(option)

    def _configure_get(self, option):
        if option in ("value", "textvariable"):
            return self._widget_cget(option)
        return super()._configure_get(option)

    def _configure_set(self, **kw):
        key = "textvariable"
        if key in kw:
            value = kw[key]
            self._entry_var = value
            self._entry.configure(textvariable=value)
        key = "value"
        if key in kw:
            value = kw.pop(key)
            self._set_value(value)
        key = "state"
        if key in kw:
            state = kw.pop(key)
            if state == "readonly":
                self._entry.configure(state=state)
                self._button.configure(state="disabled")
            else:
                self._entry.configure(state=state)
                self._button.configure(state=state)
        return super()._configure_set(**kw)

    def _set_value(self, txtcolor):
        self._color = txtcolor
        self._entry_var.set(txtcolor)
        self._show_color(txtcolor)

    def on_focusout(self, event=None):
        self.validate_change(self._entry_var.get())

    def on_keypress_after(self):
        self.validate_change(self._entry_var.get())

    def on_keypress(self, event=None):
        if self._kp_cb is not None:
            self.after_cancel(self._kp_cb)
        self._kp_cb = self.after(self.KEY_PRESS_MS, self.on_keypress_after)

    def is_color(self, txtcolor):
        try:
            self.winfo_rgb(txtcolor)
            return True
        except tk.TclError:
            pass
        return False

    def on_picker_clicked(self):
        current = self._entry_var.get()
        current = current if self.is_color(current) else None
        txtcolor = None
        _, txtcolor = tk.colorchooser.askcolor(current, parent=self)
        if txtcolor is not None:
            self._set_value(txtcolor)
            self.event_generate(self.EVENT_COLOR_CHANGED)

    def validate_change(self, newcolor):
        if self.is_color(newcolor) or newcolor == "":
            self._set_value(newcolor)
            self.event_generate(self.EVENT_COLOR_CHANGED)

    def _show_color(self, newcolor):
        newcolor = newcolor if newcolor else self.BGCOLOR
        self._frame.configure(background=newcolor)


if __name__ == "__main__":
    root = tk.Tk()
    widget = ColorInput(root)
    widget.pack(expand=True, fill="both")

    def on_color_changed(event):
        value = event.widget.cget("value")
        print(f"Color changed to: {value}")

    widget.bind(ColorInput.EVENT_COLOR_CHANGED, on_color_changed)
    widget.configure(value="brown")

    root.mainloop()
