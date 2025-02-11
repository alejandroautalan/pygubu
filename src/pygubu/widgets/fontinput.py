#!/usr/bin/python3
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font
import pygubu.widgets.fontinputui as baseui

from contextlib import suppress
from pygubu.utils.widget import WidgetConfigureMixin
from pygubu.utils.font import tkfontstr_to_dict


PREDEFINED_FONTS = [
    "TkDefaultFont",
    "TkTextFont",
    "TkFixedFont",
    "TkMenuFont",
    "TkHeadingFont",
    "TkCaptionFont",
    "TkSmallCaptionFont",
    "TkIconFont",
    "TkTooltipFont",
]

_sp = sys.platform
if _sp in ("win32", "cygwin"):
    PREDEFINED_FONTS.extend(
        ("system", "ansi", "device", "systemfixed", "ansifixed", "oemfixed")
    )
if _sp == "darwin":
    PREDEFINED_FONTS.extend(
        (
            "system",
            "application",
            "menu",
            "systemSystemFont",
            "systemEmphasizedSystemFont",
            "systemSmallSystemFont",
            "systemSmallEmphasizedSystemFont",
            "systemApplicationFont",
            "systemLabelFont",
            "systemViewsFont",
            "systemMenuTitleFont",
            "systemMenuItemFont",
            "systemMenuItemMarkFont",
            "systemMenuItemCmdKeyFont",
            "systemWindowTitleFont",
            "systemPushButtonFont",
            "systemUtilityWindowTitleFont",
            "systemAlertHeaderFont",
            "systemToolbarFont",
            "systemMiniSystemFont",
            "systemDetailSystemFont",
            "systemDetailEmphasizedSystemFont",
        )
    )


#
# Manual user code
#


class FontInput(WidgetConfigureMixin, baseui.FontInputUI):
    EVENT_FONT_CHANGED = "<<FontInput:FontChanged>>"
    KEY_PRESS_MS = 850
    FONT_SIZE_DEFAULT = None

    def __init__(self, master=None, variable: tk.Variable = None, **kw):
        super().__init__(master, **kw)
        tkvar = tk.StringVar(self, "") if variable is None else variable
        self._font_var = tkvar  # The current font value
        self._kp_cb = None
        self._fp_cb = None
        self._init_font_size()
        self._populate_options()

    @classmethod
    def _init_font_size(cls):
        if cls.FONT_SIZE_DEFAULT is None:
            font = tk.font.nametofont("TkDefaultFont")
            size = font.cget("size")
            cls.FONT_SIZE_DEFAULT = size
            print(size)

    def _widget_cget(self, option):
        if option == "value":
            return self._font_var.get()
        if option == "variable":
            return self._entry_var
        return super()._widget_cget(option)

    def _configure_get(self, option):
        if option in ("value", "variable"):
            return self._widget_cget(option)
        return super()._configure_get(option)

    def _configure_set(self, **kw):
        key = "variable"
        if key in kw:
            self._font_var = kw.pop(key)
            self._convert_to_form()
        key = "value"
        if key in kw:
            value = kw.pop(key)
            self._font_var.set(value)
            self._convert_to_form()
        key = "state"
        if key in kw:
            new_state = kw.pop(key)
            if new_state in ("normal", "disabled"):
                self.wfamily.configure(state=new_state)
                self.wsize.configure(state=new_state)
                self.wweight.configure(state=new_state)
                self.wslant.configure(state=new_state)
                self.wunderline.configure(state=new_state)
                self.woverstrike.configure(state=new_state)
        return super()._configure_set(**kw)

    def _populate_options(self):
        sizes = (
            5,
            6,
            8,
            9,
            10,
            11,
            12,
            14,
            16,
            18,
            20,
            24,
            30,
            36,
            42,
            48,
            60,
            72,
        )
        self.wsize.configure(values=sizes)

        families = sorted(tk.font.families())
        values = [""] + PREDEFINED_FONTS + families
        self.wfamily.configure(values=values)

    def _convert_to_form(self):
        if self._fp_cb is None:
            self._fp_cb = self.after_idle(self._convert_to_form_after)

    def _convert_to_form_after(self):
        self._form_clear()
        fdesc = tkfontstr_to_dict(self._font_var.get())
        key = "family"
        if fdesc[key]:
            self.family_var.set(fdesc[key])
        key = "size"
        if fdesc[key]:
            self.size_var.set(fdesc[key])
        modifiers = fdesc["modifiers"]
        if "bold" in modifiers:
            self.w_var.set(True)
        if "italic" in modifiers:
            self.s_var.set(True)
        if "underline" in modifiers:
            self.u_var.set(True)
        if "overstrike" in modifiers:
            self.o_var.set(True)
        self._form_process()

    def _value_from_form(self) -> str:
        """Process form inputs and return a tkfont description"""
        family = self.family_var.get()
        size = self.size_var.get()
        weight = self.w_var.get()
        slant = self.s_var.get()
        underline = self.u_var.get()
        overstrike = self.o_var.get()
        modifiers = []
        if weight:
            modifiers.append("bold")
        if slant:
            modifiers.append("italic")
        if underline:
            modifiers.append("underline")
        if overstrike:
            modifiers.append("overstrike")
        modifiers_str = " ".join(modifiers)
        font_tpl = "{{{family}}} {size} {{{modifiers}}}"
        return font_tpl.format(
            family=family, size=size, modifiers=modifiers_str
        )

    def _form_clear(self):
        self.family_var.set("")
        self.size_var.set("")
        self.w_var.set(False)
        self.s_var.set(False)
        self.u_var.set(False)
        self.o_var.set(False)

    def _form_process(self):
        """Process form inputs and generate the new tkfont description.
        If the value changed from original generate event."""

        family: str = self.family_var.get()
        family = family.strip()
        new_value = None
        curr_value = self._font_var.get()

        if family == "":
            # clear options
            self._form_clear()
            new_value = ""
        else:
            size = self.size_var.get()
            if size == "":
                self.size_var.set(self.FONT_SIZE_DEFAULT)
            new_value = self._value_from_form()
        if curr_value != new_value:
            self._font_var.set(new_value)
            self.event_generate(self.EVENT_FONT_CHANGED)
            print(new_value)
        self._fp_cb = None

    def on_keypress_after(self):
        self.call_process_form()

    def on_keypress(self, event=None):
        if self._kp_cb is not None:
            self.after_cancel(self._kp_cb)
        self._kp_cb = self.after(self.KEY_PRESS_MS, self.on_keypress_after)

    def on_validate_size(self, p_entry_value):
        """Allow only numbers above 0"""

        valid = False

        if p_entry_value == "":
            valid = True
        else:
            with suppress(ValueError):
                value = int(p_entry_value)
                valid = value > 0

        return valid

    def call_process_form(self, event=None):
        if self._fp_cb is None:
            self._fp_cb = self.after_idle(self._form_process)

    def on_modifier_clicked(self):
        self._form_process()


if __name__ == "__main__":
    root = tk.Tk()
    widget = FontInput(root)
    widget.configure(
        value="{Helvetica} 12 {bold}",
        # state="disabled"
    )
    widget.pack(expand=True, fill="both")
    root.mainloop()
