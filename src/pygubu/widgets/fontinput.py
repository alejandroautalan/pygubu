#!/usr/bin/python3
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font
import pygubu.widgets.fontinputui as baseui

from contextlib import suppress
from pygubu.utils.widget import WidgetConfigureMixin


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


class FontInput(baseui.FontInputUI):
    EVENT_FONT_CHANGED = "<<FontInput:FontChanged>>"
    KEY_PRESS_MS = 850
    FONT_SIZE_DEFAULT = None

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._font = ""  # The current font value
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

    def _value_from_form(self):
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

    def process_form(self):
        family = self.family_var.get()
        new_value = None

        if family == "":
            # clear options
            self.size_var.set("")
            self.w_var.set(False)
            self.s_var.set(False)
            self.u_var.set(False)
            self.o_var.set(False)
            new_value = ""
        else:
            size = self.size_var.get()
            if size == "":
                self.size_var.set(self.FONT_SIZE_DEFAULT)
            new_value = self._value_from_form()
        if self._font != new_value:
            self._font = new_value
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
            self._fp_cb = self.after_idle(self.process_form)

    def on_modifier_clicked(self):
        self.process_form()


if __name__ == "__main__":
    root = tk.Tk()
    widget = FontInput(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
