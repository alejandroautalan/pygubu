import sys
import os
import tkinter as tk
import tkinter.ttk as ttk
import math
import timeit
import logging

from tkinter import font
from dataclasses import dataclass
from ..base import IThemeBuilder
from ..color import ColorUtil
from .assets import AssetCreator
from .config import (
    FIX_LINUX_FILE_DIALOG,
    PRIMARY,
    SECONDARY,
    SUCCESS,
    INFO,
    WARNING,
    DANGER,
    LIGHT,
    DARK,
    TTK_CLAM,
    TTK_ALT,
    TTK_DEFAULT,
)

logger = logging.getLogger(__name__)


@dataclass
class Colors:
    primary: str
    secondary: str
    success: str
    info: str
    warning: str
    danger: str
    light: str
    dark: str
    # --
    bg: str
    fg: str
    selectbg: str
    selectfg: str
    border: str
    inputfg: str
    inputbg: str
    active: str

    def names(self):
        return iter(
            [
                PRIMARY,
                SECONDARY,
                SUCCESS,
                INFO,
                WARNING,
                DANGER,
                LIGHT,
                DARK,
            ]
        )

    def get_foreground(self, color_label):
        if color_label == LIGHT:
            return self.dark
        elif color_label == DARK:
            return self.light
        else:
            return self.selectfg

    def get_color(self, name):
        return getattr(self, name)


class ThemeDefinition:
    THEME_LIGHT = LIGHT
    THEME_DARK = DARK

    def __init__(self, name: str, colors: dict, theme_type=THEME_LIGHT):
        self.name = name
        self.colors = Colors(**colors)
        self.type = theme_type


_colect_styles = bool(os.getenv("PYGUBU_DESIGNER_RUNNING"))
has_tk_version_9 = tk.TkVersion >= 9


class BootstrapThemeBuilder(IThemeBuilder):
    generated_styles = set()

    def __init__(self, theme_def):
        self.theme = theme_def
        self.tk_master = None
        self.colorutil = None
        self.existing_elements = {}
        self.assets = AssetCreator(self)
        self.tk_widgets_options = {}

    def theme_name(self):
        return self.theme.name

    def theme_parent(self):
        return "clam"

    def theme_settings(self):
        return self.build_theme_settings()

    def tk_palette(self):
        return self.build_tk_palette()

    def db_settings(self):
        self.build_tk_widget_settings()
        db = {}
        for widget, options in self.tk_widgets_options.items():
            pattern = f"*{widget}."
            db[pattern] = options.copy()
        return db

    def create(self, master):
        self.tk_master = master
        self.colorutil = ColorUtil(master)
        super().create(master)

        if sys.platform == "linux" and FIX_LINUX_FILE_DIALOG:
            self._install_linux_filedialog_hack(master)

    def apply(self, master: tk.Widget):
        super().apply(master)

        if sys.platform == "linux" and FIX_LINUX_FILE_DIALOG:
            self._update_linux_filedialog_bg(master)

    def _get_filedialog_bg_color(self):
        color = self.colors.bg if self.is_light_theme else self.colors.selectbg
        color = self.colorutil.update_hsv(color, vd=0.18)
        return color

    def _install_linux_filedialog_hack(self, master):
        """Install script to modify dialog background color.
        For now, this only works for the first time the dialog window is created.
        """
        script = """
# Enable filedialog namespace
catch {tk_getOpenFile -badoption}

# Install hack function
if { [info exists ::tk::dialog::file::pbs_hack ] == 0 } {
  set ::tk::dialog::file::pbs_hack 1
  # Set color for background
  set ::tk::dialog::file::pbs_filedialog_bg {color}

  rename ::tk::dialog::file::Create ::tk::dialog::file::_pbs_filedialog_create
  proc ::tk::dialog::file::Create {w class} {
    eval ::tk::dialog::file::_pbs_filedialog_create $w $class
    $w.contents.icons.cHull.canvas configure -background $::tk::dialog::file::pbs_filedialog_bg
  }
}
"""
        script = script.replace("{color}", self._get_filedialog_bg_color())
        master.tk.eval(script)

    def _update_linux_filedialog_bg(self, master):
        script = """
if { [info exists ::tk::dialog::file::pbs_hack ] == 1 } {
  set ::tk::dialog::file::pbs_filedialog_bg {color}
}
"""
        script = script.replace("{color}", self._get_filedialog_bg_color())
        master.tk.eval(script)

    def update_current_widgets(self, master):
        if not isinstance(master, tk.Tk):
            master = master.winfo_toplevel()
        style = ttk.Style(self.tk_master)
        self._walk_and_update_widget(master, style)

    def _walk_and_update_widget(self, widget, style, level=0):
        if isinstance(widget, tk.Misc):
            wclass = widget.winfo_class()
            # wstyle = None
            if isinstance(widget, ttk.Widget) and wclass == "TCombobox":
                # wstyle = widget.cget("style")
                # curr_style = wstyle if wstyle else wclass
                self.update_combobox_popdown_style(widget)
            else:
                if wclass in self.tk_widgets_options:
                    # some widget may block the property (like customtkinter)
                    # so add try here.
                    try:
                        widget.configure(**self.tk_widgets_options[wclass])
                    except Exception as e:
                        logger.debug(e)
            # print("  " * level, f"{wclass} {wstyle}")
            for k, v in widget.children.items():
                self._walk_and_update_widget(v, style, level + 1)

    @property
    def colors(self):
        return self.theme.colors

    @property
    def is_light_theme(self):
        return self.theme.type == ThemeDefinition.THEME_LIGHT

    def scale_size(self, size):
        """Scale the size of images and other assets based on the
        scaling factor of ttk to ensure that the image matches the
        screen resolution.

        Parameters:

            size (Union[int, List, Tuple]):
                A single integer or an iterable of integers
        """
        winsys = self.tk_master.tk.call("tk", "windowingsystem")
        if winsys == "aqua":
            BASELINE = 1.000492368291482
        else:
            BASELINE = 1.33398982438864281
        scaling = self.tk_master.tk.call("tk", "scaling")
        factor = scaling / BASELINE

        if isinstance(size, int) or isinstance(size, float):
            return math.ceil(size * factor)
        elif isinstance(size, tuple) or isinstance(size, list):
            return [math.ceil(x * factor) for x in size]

    def build_tk_widget_settings(self):
        # widget.option_add('*Text*Font', 'TkDefaultFont')
        wo = {
            "Tk": {"background": self.colors.bg},
            "Toplevel": {"background": self.colors.bg},
            "Canvas": {
                "background": self.colors.bg,
                "highlightthickness": 0,
            },
            "Label": {
                "foreground": self.colors.fg,
                "background": self.colors.bg,
            },
            "Frame": {"background": self.colors.bg},
            "Checkbutton": {
                "activebackground": self.colors.bg,
                "activeforeground": self.colors.primary,
                "background": self.colors.bg,
                "foreground": self.colors.fg,
                "selectcolor": self.colors.bg,
            },
            "Radiobutton": {
                "activebackground": self.colors.bg,
                "activeforeground": self.colors.primary,
                "background": self.colors.bg,
                "foreground": self.colors.fg,
                "selectcolor": self.colors.bg,
            },
            "Menu": {
                "tearoff": False,
                "activebackground": self.colors.selectbg,
                "activeforeground": self.colors.selectfg,
                "foreground": self.colors.fg,
                "selectcolor": self.colors.primary,
                "background": self.colors.bg,
                "relief": tk.FLAT,
                "borderwidth": 0,
            },
        }
        # buttons
        background = self.colors.primary
        foreground = self.colors.selectfg
        activebackground = self.colorutil.update_hsv(
            self.colors.primary, vd=-0.1
        )
        wo["Button"] = {
            "background": background,
            "foreground": foreground,
            "relief": tk.FLAT,
            "borderwidth": 0,
            "activebackground": activebackground,
            "highlightbackground": self.colors.selectfg,
        }
        # Entry
        bordercolor = (
            self.colors.border if self.is_light_theme else self.colors.selectbg
        )
        wo["Entry"] = {
            "relief": tk.FLAT,
            "highlightthickness": 1,
            "foreground": self.colors.inputfg,
            "highlightbackground": bordercolor,
            "highlightcolor": self.colors.primary,
            "background": self.colors.inputbg,
            "insertbackground": self.colors.inputfg,
            "insertwidth": 1,
        }
        # Scale
        bordercolor = (
            self.colors.border if self.is_light_theme else self.colors.selectbg
        )
        activecolor = self.colorutil.update_hsv(self.colors.primary, vd=-0.2)
        wo["Scale"] = {
            "background": self.colors.primary,
            "showvalue": False,
            "sliderrelief": tk.FLAT,
            "borderwidth": 0,
            "activebackground": activecolor,
            "highlightthickness": 1,
            "highlightcolor": bordercolor,
            "highlightbackground": bordercolor,
            "troughcolor": self.colors.inputbg,
        }
        # Spinbox
        bordercolor = (
            self.colors.border if self.is_light_theme else self.colors.selectbg
        )
        wo["Spinbox"] = {
            "relief": tk.FLAT,
            "highlightthickness": 1,
            "foreground": self.colors.inputfg,
            "highlightbackground": bordercolor,
            "highlightcolor": self.colors.primary,
            "background": self.colors.inputbg,
            "buttonbackground": self.colors.inputbg,
            "insertbackground": self.colors.inputfg,
            "insertwidth": 1,
            # these options should work, but do not have any affect
            "buttonuprelief": tk.FLAT,
            "buttondownrelief": tk.SUNKEN,
        }
        # Listbox
        bordercolor = (
            self.colors.border if self.is_light_theme else self.colors.selectbg
        )
        wo["Spinbox"] = {
            "foreground": self.colors.inputfg,
            "background": self.colors.inputbg,
            "selectbackground": self.colors.selectbg,
            "selectforeground": self.colors.selectfg,
            "highlightcolor": self.colors.primary,
            "highlightbackground": bordercolor,
            "highlightthickness": 1,
            "activestyle": "none",
            "relief": tk.FLAT,
        }
        # Menubutton
        activebackground = self.colorutil.update_hsv(
            self.colors.primary, vd=-0.2
        )
        wo["Menubutton"] = {
            "background": self.colors.primary,
            "foreground": self.colors.selectfg,
            "activebackground": activebackground,
            "activeforeground": self.colors.selectfg,
            "borderwidth": 0,
        }
        # LabelFrame
        bordercolor = (
            self.colors.border if self.is_light_theme else self.colors.selectbg
        )
        wo["LabelFrame"] = {
            "highlightcolor": bordercolor,
            "foreground": self.colors.fg,
            "borderwidth": 1,
            "highlightthickness": 0,
            "background": self.colors.bg,
        }
        # Text
        bordercolor = (
            self.colors.border if self.is_light_theme else self.colors.selectbg
        )
        focuscolor = bordercolor
        wo["Text"] = {
            "background": self.colors.inputbg,
            "foreground": self.colors.inputfg,
            "highlightcolor": focuscolor,
            "highlightbackground": bordercolor,
            "insertbackground": self.colors.inputfg,
            "selectbackground": self.colors.selectbg,
            "selectforeground": self.colors.selectfg,
            "insertwidth": 1,
            "highlightthickness": 1,
            "relief": tk.FLAT,
            "padx": 5,
            "pady": 5,
        }
        self.tk_widgets_options = wo

    def build_theme_settings(self):
        tstart = timeit.default_timer()
        settings = {}
        self.create_default_style(settings)

        colornames = [c for c in self.colors.names()]
        colornames.insert(0, None)
        for name in colornames:
            # Frames
            self.create_frame_style(settings, name)
            self.create_labelframe_style(settings, name)
            # Labels
            self.create_label_style(settings, name)
            self.create_inverse_label_style(settings, name)
            # Buttons
            self.create_button_style(settings, name)
            self.create_toolbutton_style(settings, name)
            self.create_outline_button_style(settings, name)
            self.create_outline_menubutton_style(settings, name)
            self.create_outline_toolbutton_style(settings, name)
            self.create_link_button_style(settings, name)
            self.create_radiobutton_style(settings, name)
            self.create_menubutton_style(settings, name)
            self.create_checkbutton_style(settings, name)
            self.create_square_toggle_style(settings, name)
            self.create_round_toggle_style(settings, name)
            # Entry
            self.create_entry_style(settings, name)
            # Combo
            self.create_combobox_style(settings, name)
            # Panedwindow
            self.create_panedwindow_style(settings, name)
            # Notebook
            self.create_notebook_style(settings, name)
            # separator
            self.create_separator_style(settings, name)
            # Progress bars
            self.create_progressbar_style(settings, name)
            self.create_striped_progressbar_style(settings, name)
            # Scale
            self.create_scale_style(settings, name)
            # scrollbar
            self.create_scrollbar_style(settings, name)
            self.create_round_scrollbar_style(settings, name)
            # spinbox
            self.create_spinbox_style(settings, name)
            # treeview
            self.create_treeview_style(settings, name)
            self.create_table_treeview_style(settings, name)
            # sizegrip
            self.create_sizegrip_style(settings, name)
            # Floodgauge
            self.create_floodgauge_style(settings, name)

        tfinish = timeit.default_timer() - tstart
        logger.debug("Bootstrap ttk theme build time: %s", tfinish)
        return settings

    def build_tk_palette(self):
        return {
            "background": self.colors.bg,
            "foreground": self.colors.fg,
            "highlightColor": self.colors.primary,
            "selectBackground": self.colors.selectbg,
            "selectForeground": self.colors.selectfg,
            "activeBackground": self.colors.selectbg,
            "activeForeground": self.colors.selectfg,
        }

    def _register_style(self, style_name):
        if _colect_styles:
            self.generated_styles.add(style_name)

    def update_combobox_popdown_style(self, widget):
        """Update the legacy ttk.Combobox elements. This method is
        called every time the theme is changed in order to ensure
        that the legacy tkinter components embedded in this ttk widget
        are styled appropriate to the current theme.

        The ttk.Combobox contains several elements that are not styled
        using the ttk theme engine. This includes the **popdownwindow**
        and the **scrollbar**. Both of these widgets are configured
        manually using calls to tcl/tk.

        Parameters:

            widget (ttk.Combobox):
                The combobox element to be updated.
        """
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        tk_settings = []
        tk_settings.extend(["-borderwidth", 2])
        tk_settings.extend(["-highlightthickness", 1])
        tk_settings.extend(["-highlightcolor", bordercolor])
        tk_settings.extend(["-background", self.colors.inputbg])
        tk_settings.extend(["-foreground", self.colors.inputfg])
        tk_settings.extend(["-selectbackground", self.colors.selectbg])
        tk_settings.extend(["-selectforeground", self.colors.selectfg])

        # set popdown style
        popdown = widget.tk.eval(f"ttk::combobox::PopdownWindow {widget}")
        widget.tk.call(f"{popdown}.f.l", "configure", *tk_settings)

        # set scrollbar style
        sb_style = "TCombobox.Vertical.TScrollbar"
        widget.tk.call(f"{popdown}.f.sb", "configure", "-style", sb_style)

    def create_default_style(self, settings: dict):
        settings["."] = {
            "configure": {
                "background": self.colors.bg,
                "darkcolor": self.colors.border,
                "foreground": self.colors.fg,
                "troughcolor": self.colors.bg,
                "selectbg": self.colors.selectbg,
                "selectfg": self.colors.selectfg,
                "selectbackground": self.colors.selectbg,
                "selectforeground": self.colors.selectfg,
                "fieldbackground": self.colors.bg,
                # "font": "TkDefaultFont",
                "borderwidth": 1,
                "focuscolor": "",
            },
        }

    def create_frame_style(self, settings, colorname=None):
        """Create a style for the ttk.Frame widget."""
        STYLE = "TFrame"

        if any([colorname is None, not colorname]):
            ttkstyle = STYLE
            background = self.colors.bg
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            background = self.colors.get_color(colorname)

        settings[ttkstyle] = {
            "configure": {
                "background": background,
            }
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_labelframe_style(self, settings, colorname=None):
        """Create a style for the ttk.Labelframe widget."""
        STYLE = "TLabelframe"

        background = self.colors.bg

        if any([colorname is None, not colorname]):
            foreground = self.colors.fg
            ttkstyle = STYLE

            if self.is_light_theme:
                bordercolor = self.colors.border
            else:
                bordercolor = self.colors.selectbg

        else:
            foreground = self.colors.get_color(colorname)
            bordercolor = foreground
            ttkstyle = f"{colorname}.{STYLE}"

        settings[f"{ttkstyle}.Label"] = {
            "configure": {
                "foreground": foreground,
                "background": background,
            }
        }
        settings[ttkstyle] = {
            "configure": {
                "relief": tk.RAISED,
                "borderwidth": 1,
                "bordercolor": bordercolor,
                "lightcolor": background,
                "darkcolor": background,
                "background": background,
            }
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_label_style(self, settings, colorname=None):
        """Create a standard style for the ttk.Label widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TLabel"

        if any([colorname is None, colorname == ""]):
            ttkstyle = STYLE
            foreground = self.colors.fg
            background = self.colors.bg
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get_color(colorname)
            background = self.colors.bg

        # standard label
        settings[ttkstyle] = {
            "configure": {"foreground": foreground, "background": background}
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_inverse_label_style(self, settings, colorname=None):
        """Create an inverted style for the ttk.Label."""
        STYLE_INVERSE = "Inverse.TLabel"

        if any([colorname is None, not colorname]):
            ttkstyle = STYLE_INVERSE
            background = self.colors.fg
            foreground = self.colors.bg
        else:
            ttkstyle = f"{colorname}.{STYLE_INVERSE}"
            background = self.colors.get_color(colorname)
            foreground = self.colors.get_foreground(colorname)

        settings[ttkstyle] = {
            "configure": {"foreground": foreground, "background": background}
        }
        self._register_style(ttkstyle)

    def create_button_style(self, settings, colorname=None):
        STYLE = "TButton"

        if any([colorname is None, colorname == ""]):
            ttkstyle = STYLE
            foreground = self.colors.get_foreground(PRIMARY)
            background = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get_foreground(colorname)
            background = self.colors.get_color(colorname)

        bordercolor = background
        disabled_bg = self.colorutil.make_transparent(
            0.10, self.colors.fg, self.colors.bg
        )
        disabled_fg = self.colorutil.make_transparent(
            0.30, self.colors.fg, self.colors.bg
        )
        pressed = self.colorutil.make_transparent(
            0.80, background, self.colors.bg
        )
        hover = self.colorutil.make_transparent(
            0.90, background, self.colors.bg
        )

        settings[ttkstyle] = {
            "configure": {
                "foreground": foreground,
                "background": background,
                "bordercolor": bordercolor,
                "darkcolor": background,
                "lightcolor": background,
                "relief": tk.RAISED,
                "focusthickness": 0,
                "focuscolor": foreground,
                "padding": (10, 5),
                "anchor": tk.CENTER,
            },
            "map": {
                "foreground": [("disabled", disabled_fg)],
                "background": [
                    ("disabled", disabled_bg),
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "bordercolor": [("disabled", disabled_bg)],
                "darkcolor": [
                    ("disabled", disabled_bg),
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "lightcolor": [
                    ("disabled", disabled_bg),
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
            },
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_toolbutton_style(self, settings, colorname=None):
        """Create a solid toolbutton style for the ttk.Checkbutton"""
        STYLE = "Toolbutton"

        if any([colorname is None, colorname == ""]):
            ttkstyle = STYLE
            toggle_on = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            toggle_on = self.colors.get_color(colorname)

        foreground = self.colors.get_foreground(colorname)

        if self.is_light_theme:
            toggle_off = self.colors.border
        else:
            toggle_off = self.colors.selectbg

        disabled_bg = self.colorutil.make_transparent(
            0.10, self.colors.fg, self.colors.bg
        )
        disabled_fg = self.colorutil.make_transparent(
            0.30, self.colors.fg, self.colors.bg
        )

        settings[ttkstyle] = {
            "configure": {
                "foreground": self.colors.selectfg,
                "background": toggle_off,
                "bordercolor": toggle_off,
                "darkcolor": toggle_off,
                "lightcolor": toggle_off,
                "relief": tk.RAISED,
                "focusthickness": 0,
                "focuscolor": "",
                "padding": (10, 5),
                "anchor": tk.CENTER,
            },
            "map": {
                "foreground": [
                    ("disabled", disabled_fg),
                    ("hover", foreground),
                    ("selected", foreground),
                ],
                "background": [
                    ("disabled", disabled_bg),
                    ("pressed !disabled", toggle_on),
                    ("selected !disabled", toggle_on),
                    ("hover !disabled", toggle_on),
                ],
                "bordercolor": [
                    ("disabled", disabled_bg),
                    ("pressed !disabled", toggle_on),
                    ("selected !disabled", toggle_on),
                    ("hover !disabled", toggle_on),
                ],
                "darkcolor": [
                    ("disabled", disabled_bg),
                    ("pressed !disabled", toggle_on),
                    ("selected !disabled", toggle_on),
                    ("hover !disabled", toggle_on),
                ],
                "lightcolor": [
                    ("disabled", disabled_bg),
                    ("pressed !disabled", toggle_on),
                    ("selected !disabled", toggle_on),
                    ("hover !disabled", toggle_on),
                ],
            },
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_outline_button_style(self, settings, colorname=None):
        """Create an outline style for the ttk.Button widget."""
        STYLE = "Outline.TButton"

        disabled_fg = self.colorutil.make_transparent(
            0.30, self.colors.fg, self.colors.bg
        )

        if any([colorname is None, not colorname]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        foreground = self.colors.get_color(colorname)
        background = self.colors.get_foreground(colorname)
        foreground_pressed = background
        bordercolor = foreground
        pressed = foreground
        hover = foreground

        settings[ttkstyle] = {
            "configure": {
                "foreground": foreground,
                "background": self.colors.bg,
                "bordercolor": bordercolor,
                "darkcolor": self.colors.bg,
                "lightcolor": self.colors.bg,
                "relief": tk.RAISED,
                "focusthickness": 0,
                "focuscolor": foreground,
                "padding": (10, 5),
                "anchor": tk.CENTER,
            },
            "map": {
                "foreground": [
                    ("disabled", disabled_fg),
                    ("pressed !disabled", foreground_pressed),
                    ("hover !disabled", foreground_pressed),
                ],
                "background": [
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "bordercolor": [
                    ("disabled", disabled_fg),
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "darkcolor": [
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "lightcolor": [
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "focuscolor": [
                    ("pressed !disabled", foreground_pressed),
                    ("hover !disabled", foreground_pressed),
                ],
            },
        }
        self._register_style(ttkstyle)

    def create_outline_menubutton_style(self, settings, colorname=None):
        """Create an outline button style for the ttk.Menubutton widget"""
        STYLE = "Outline.TMenubutton"

        disabled_fg = self.colorutil.make_transparent(
            0.30, self.colors.fg, self.colors.bg
        )

        if any([colorname is None, not colorname]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        foreground = self.colors.get_color(colorname)
        background = self.colors.get_foreground(colorname)
        foreground_pressed = background
        bordercolor = foreground
        pressed = foreground
        hover = foreground

        settings[ttkstyle] = {
            "configure": {
                "foreground": foreground,
                "background": self.colors.bg,
                "bordercolor": bordercolor,
                "darkcolor": self.colors.bg,
                "lightcolor": self.colors.bg,
                "relief": tk.RAISED,
                "focusthickness": 0,
                "focuscolor": foreground,
                "padding": (10, 5),
                "arrowcolor": foreground,
                "arrowpadding": (0, 0, 15, 0),
                "arrowsize": self.scale_size(4),
            },
            "map": {
                "foreground": [
                    ("disabled", disabled_fg),
                    ("pressed !disabled", foreground_pressed),
                    ("hover !disabled", foreground_pressed),
                ],
                "background": [
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "bordercolor": [
                    ("disabled", disabled_fg),
                    ("pressed", pressed),
                    ("hover", hover),
                ],
                "darkcolor": [
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "lightcolor": [
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "arrowcolor": [
                    ("disabled", disabled_fg),
                    ("pressed", foreground_pressed),
                    ("hover", foreground_pressed),
                ],
            },
        }
        self._register_style(ttkstyle)

    def create_outline_toolbutton_style(self, settings, colorname=None):
        """Create an outline toolbutton style for the ttk.Checkbutton
        and ttk.Radiobutton widgets.
        """
        STYLE = "Outline.Toolbutton"

        disabled_fg = self.colorutil.make_transparent(
            0.30, self.colors.fg, self.colors.bg
        )

        if any([colorname is None, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        foreground = self.colors.get_color(colorname)
        background = self.colors.get_foreground(colorname)
        foreground_pressed = background
        bordercolor = foreground
        pressed = foreground
        hover = foreground

        settings[ttkstyle] = {
            "configure": {
                "foreground": foreground,
                "background": self.colors.bg,
                "bordercolor": bordercolor,
                "darkcolor": self.colors.bg,
                "lightcolor": self.colors.bg,
                "relief": tk.RAISED,
                "focusthickness": 0,
                "focuscolor": foreground,
                "padding": (10, 5),
                "anchor": tk.CENTER,
                "arrowcolor": foreground,
                "arrowpadding": (0, 0, 15, 0),
                "arrowsize": 3,
            },
            "map": {
                "foreground": [
                    ("disabled", disabled_fg),
                    ("pressed !disabled", foreground_pressed),
                    ("selected !disabled", foreground_pressed),
                    ("hover !disabled", foreground_pressed),
                ],
                "background": [
                    ("pressed !disabled", pressed),
                    ("selected !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "bordercolor": [
                    ("disabled", disabled_fg),
                    ("pressed !disabled", pressed),
                    ("selected !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "darkcolor": [
                    ("disabled", self.colors.bg),
                    ("pressed !disabled", pressed),
                    ("selected !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "lightcolor": [
                    ("disabled", self.colors.bg),
                    ("pressed !disabled", pressed),
                    ("selected !disabled", pressed),
                    ("hover !disabled", hover),
                ],
            },
        }
        self._register_style(ttkstyle)

    def create_link_button_style(self, settings, colorname=None):
        """Create a link button style for the ttk.Button widget."""
        STYLE = "Link.TButton"

        pressed = self.colors.info
        hover = self.colors.info

        if any([colorname is None, not colorname]):
            foreground = self.colors.fg
            ttkstyle = STYLE
        elif colorname == LIGHT:
            foreground = self.colors.fg
            ttkstyle = f"{colorname}.{STYLE}"
        else:
            foreground = self.colors.get_color(colorname)
            ttkstyle = f"{colorname}.{STYLE}"

        disabled_fg = self.colorutil.make_transparent(
            0.30, self.colors.fg, self.colors.bg
        )

        settings[ttkstyle] = {
            "configure": {
                "foreground": foreground,
                "background": self.colors.bg,
                "bordercolor": self.colors.bg,
                "darkcolor": self.colors.bg,
                "lightcolor": self.colors.bg,
                "relief": tk.RAISED,
                "focusthickness": 0,
                "focuscolor": foreground,
                "anchor": tk.CENTER,
                "padding": (10, 5),
            },
            "map": {
                "shiftrelief=": [("pressed !disabled", -1)],
                "foreground": [
                    ("disabled", disabled_fg),
                    ("pressed", "!disabled", pressed),
                    ("hover", "!disabled", hover),
                ],
                "focuscolor": [
                    ("pressed !disabled", pressed),
                    ("hover", "!disabled", pressed),
                ],
                "background": [
                    ("disabled", self.colors.bg),
                    ("pressed !disabled", self.colors.bg),
                    ("hover", "!disabled", self.colors.bg),
                ],
                "bordercolor": [
                    ("disabled", self.colors.bg),
                    ("pressed !disabled", self.colors.bg),
                    ("hover !disabled", self.colors.bg),
                ],
                "darkcolor": [
                    ("disabled", self.colors.bg),
                    ("pressed !disabled", self.colors.bg),
                    ("hover !disabled", self.colors.bg),
                ],
                "lightcolor": [
                    ("disabled", self.colors.bg),
                    ("pressed !disabled", self.colors.bg),
                    ("hover !disabled", self.colors.bg),
                ],
            },
        }
        self._register_style(ttkstyle)

    def create_entry_style(self, settings, colorname=None):
        """Create a style for the ttk.Entry widget."""
        STYLE = "TEntry"

        # general default colors
        if self.is_light_theme:
            disabled_fg = self.colors.border
            bordercolor = self.colors.border
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        if any([colorname is None, not colorname]):
            # default style
            ttkstyle = STYLE
            focuscolor = self.colors.primary
        else:
            # colored style
            ttkstyle = f"{colorname}.{STYLE}"
            focuscolor = self.colors.get_color(colorname)
            bordercolor = focuscolor

        settings[ttkstyle] = {
            "configure": {
                "bordercolor": bordercolor,
                "darkcolor": self.colors.inputbg,
                "lightcolor": self.colors.inputbg,
                "fieldbackground": self.colors.inputbg,
                "foreground": self.colors.inputfg,
                "insertcolor": self.colors.inputfg,
                "padding": 5,
            },
            "map": {
                "foreground": [("disabled", disabled_fg)],
                "fieldbackground": [("readonly", readonly)],
                "bordercolor": [
                    ("invalid", self.colors.danger),
                    ("focus !disabled", focuscolor),
                    ("hover !disabled", focuscolor),
                ],
                "lightcolor": [
                    ("focus invalid", self.colors.danger),
                    ("focus !disabled", focuscolor),
                    ("readonly", readonly),
                ],
                "darkcolor": [
                    ("focus invalid", self.colors.danger),
                    ("focus !disabled", focuscolor),
                    ("readonly", readonly),
                ],
            },
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_menubutton_style(self, settings, colorname=None):
        """Create a solid style for the ttk.Menubutton widget."""
        STYLE = "TMenubutton"

        foreground = self.colors.get_foreground(colorname)

        if any([colorname is None, not colorname]):
            ttkstyle = STYLE
            background = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            background = self.colors.get_color(colorname)

        disabled_bg = self.colorutil.make_transparent(
            0.10, self.colors.fg, self.colors.bg
        )
        disabled_fg = self.colorutil.make_transparent(
            0.30, self.colors.fg, self.colors.bg
        )
        pressed = self.colorutil.make_transparent(
            0.80, background, self.colors.bg
        )
        hover = self.colorutil.make_transparent(
            0.90, background, self.colors.bg
        )

        settings[ttkstyle] = {
            "configure": {
                "foreground": foreground,
                "background": background,
                "bordercolor": background,
                "darkcolor": background,
                "lightcolor": background,
                "arrowsize": self.scale_size(4),
                "arrowcolor": foreground,
                "arrowpadding": (0, 0, 15, 0),
                "relief": tk.RAISED,
                "focusthickness": 0,
                "focuscolor": self.colors.selectfg,
                "padding": (10, 5),
            },
            "map": {
                "arrowcolor": [("disabled", disabled_fg)],
                "foreground": [("disabled", disabled_fg)],
                "background": [
                    ("disabled", disabled_bg),
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "bordercolor": [
                    ("disabled", disabled_bg),
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "darkcolor": [
                    ("disabled", disabled_bg),
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
                "lightcolor": [
                    ("disabled", disabled_bg),
                    ("pressed !disabled", pressed),
                    ("hover !disabled", hover),
                ],
            },
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_combobox_style(self, settings, colorname=None):
        """Create a style for the ttk.Combobox widget."""
        STYLE = "TCombobox"

        if self.is_light_theme:
            disabled_fg = self.colors.border
            bordercolor = self.colors.border
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        if any([colorname is None, not colorname]):
            ttkstyle = STYLE
            element = f"{ttkstyle.replace('TC', 'C')}"
            focuscolor = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            element = f"{ttkstyle.replace('TC', 'C')}"
            focuscolor = self.colors.get_color(colorname)

        if all([colorname, colorname is not None]):
            bordercolor = focuscolor

        ttk_elements = (
            (f"{element}.downarrow", TTK_DEFAULT),
            (f"{element}.padding", TTK_CLAM),
            (f"{element}.textarea", TTK_CLAM),
        )
        for element_name, from_ in ttk_elements:
            settings[element_name] = {
                "element create": ("from", from_),
            }

        settings[ttkstyle] = {
            "configure": {
                "bordercolor": bordercolor,
                "darkcolor": self.colors.inputbg,
                "lightcolor": self.colors.inputbg,
                "arrowcolor": self.colors.inputfg,
                "foreground": self.colors.inputfg,
                "fieldbackground": self.colors.inputbg,
                "background": self.colors.inputbg,
                "insertcolor": self.colors.inputfg,
                "relief": tk.FLAT,
                "padding": 5,
                "arrowsize": self.scale_size(12),
            },
            "map": {
                "background": [("readonly", readonly)],
                "fieldbackground": [("readonly", readonly)],
                "foreground": [("disabled", disabled_fg)],
                "bordercolor": [
                    ("invalid", self.colors.danger),
                    ("focus !disabled", focuscolor),
                    ("hover !disabled", focuscolor),
                ],
                "lightcolor": [
                    ("focus invalid", self.colors.danger),
                    ("focus !disabled", focuscolor),
                    ("pressed !disabled", focuscolor),
                    ("readonly", readonly),
                ],
                "darkcolor": [
                    ("focus invalid", self.colors.danger),
                    ("focus !disabled", focuscolor),
                    ("pressed !disabled", focuscolor),
                    ("readonly", readonly),
                ],
                "arrowcolor": [
                    ("disabled", disabled_fg),
                    ("pressed !disabled", focuscolor),
                    ("focus !disabled", focuscolor),
                    ("hover !disabled", focuscolor),
                ],
            },
            "layout": [
                (
                    "combo.Spinbox.field",
                    {
                        "side": tk.TOP,
                        "sticky": tk.EW,
                        "children": [
                            (
                                "Combobox.downarrow",
                                {"side": tk.RIGHT, "sticky": tk.NS},
                            ),
                            (
                                "Combobox.padding",
                                {
                                    "expand": "1",
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            "Combobox.textarea",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                },
                            ),
                        ],
                    },
                )
            ],
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_panedwindow_style(self, settings, colorname=None):
        """Create a standard style for the ttk.Panedwindow widget."""
        H_STYLE = "Horizontal.TPanedwindow"
        V_STYLE = "Vertical.TPanedwindow"

        if self.is_light_theme:
            default_color = self.colors.border
        else:
            default_color = self.colors.selectbg

        if any([colorname is None, not colorname]):
            sashcolor = default_color
            h_ttkstyle = H_STYLE
            v_ttkstyle = V_STYLE
        else:
            sashcolor = self.colors.get_color(colorname)
            h_ttkstyle = f"{colorname}.{H_STYLE}"
            v_ttkstyle = f"{colorname}.{V_STYLE}"

        settings["Sash"] = {
            "configure": {"gripcount": 0, "sashthickness": self.scale_size(2)}
        }
        settings[h_ttkstyle] = {
            "configure": {
                "background": sashcolor,
            }
        }
        settings[v_ttkstyle] = {
            "configure": {
                "background": sashcolor,
            }
        }
        if colorname:
            self._register_style(h_ttkstyle)
            self._register_style(v_ttkstyle)

    def create_notebook_style(self, settings, colorname=None):
        """Create a standard style for the ttk.Notebook widget."""
        STYLE = "TNotebook"

        if self.is_light_theme:
            bordercolor = self.colors.border
            foreground = self.colors.inputfg
        else:
            bordercolor = self.colors.selectbg
            foreground = self.colors.selectfg

        if any([colorname is None, not colorname]):
            background = self.colors.inputbg
            selectfg = self.colors.fg
            ttkstyle = STYLE
        else:
            selectfg = self.colors.get_foreground(colorname)
            background = self.colors.get_color(colorname)
            ttkstyle = f"{colorname}.{STYLE}"

        ttkstyle_tab = f"{ttkstyle}.Tab"

        # create widget style
        settings[ttkstyle] = {
            "configure": {
                "background": self.colors.bg,
                "bordercolor": bordercolor,
                "lightcolor": self.colors.bg,
                "darkcolor": self.colors.bg,
                "tabmargins": (0, 1, 1, 0),
            }
        }
        settings[ttkstyle_tab] = {
            "configure": {
                "focuscolor": "",
                "foreground": foreground,
                "padding": (6, 5),
            },
            "map": {
                "background": [
                    ("selected", self.colors.bg),
                    ("!selected", background),
                ],
                "lightcolor": [
                    ("selected", self.colors.bg),
                    ("!selected", background),
                ],
                "bordercolor": [
                    ("selected", bordercolor),
                    ("!selected", bordercolor),
                ],
                "padding": [("selected", (6, 5)), ("!selected", (6, 5))],
                "foreground": [
                    ("selected", foreground),
                    ("!selected", selectfg),
                ],
            },
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_separator_style(self, settings, colorname=None):
        """Create a style for the ttk.Separator widget."""
        HSTYLE = "Horizontal.TSeparator"
        VSTYLE = "Vertical.TSeparator"

        hsize = [20, 1]
        # vsize = [1, 40]

        # style colors
        if self.is_light_theme:
            default_color = self.colors.border
        else:
            default_color = self.colors.selectbg

        if any([colorname is None, not colorname]):
            background = default_color
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
        else:
            background = self.colors.get_color(colorname)
            h_ttkstyle = f"{colorname}.{HSTYLE}"
            v_ttkstyle = f"{colorname}.{VSTYLE}"

        # assets
        h_name, v_name = self.assets.create_separator_assets(hsize, background)

        # horizontal separator
        h_element = h_ttkstyle.replace(".TS", ".S")
        h_element_uid = f"{h_element}.separator"
        settings[h_element_uid] = {
            "element create": ("image", h_name),
        }
        settings[h_ttkstyle] = {"layout": [(h_element_uid, {"sticky": tk.EW})]}

        # vertical separator
        v_element = v_ttkstyle.replace(".TS", ".S")
        v_element_uid = f"{v_element}.separator"
        settings[v_element_uid] = {
            "element create": ("image", v_name),
        }
        settings[v_ttkstyle] = {"layout": [(v_element_uid, {"sticky": tk.NS})]}
        if colorname:
            self._register_style(h_ttkstyle)
            self._register_style(v_ttkstyle)

    def create_progressbar_style(self, settings, colorname=None):
        """Create a solid ttk style for the ttk.Progressbar widget."""
        H_STYLE = "Horizontal.TProgressbar"
        V_STYLE = "Vertical.TProgressbar"

        thickness = self.scale_size(10)

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
                bordercolor = self.colors.light
            else:
                troughcolor = self.colors.light
                bordercolor = troughcolor
        else:
            troughcolor = self.colorutil.update_hsv(
                self.colors.selectbg, vd=-0.2
            )
            bordercolor = troughcolor

        if any([colorname is None, not colorname]):
            background = self.colors.primary
            foreground = self.colors.fg
            h_ttkstyle = H_STYLE
            v_ttkstyle = V_STYLE
        else:
            background = self.colors.get_color(colorname)
            foreground = self.colors.get_color(colorname)
            h_ttkstyle = f"{colorname}.{H_STYLE}"
            v_ttkstyle = f"{colorname}.{V_STYLE}"

        # horizontal progressbar
        h_element = h_ttkstyle.replace(".TP", ".P")
        htrough_element = f"{h_element}.trough"
        hpbar_element = f"{h_element}.pbar"
        hpbar_text_element = f"{h_element}.ctext"

        if htrough_element not in self.existing_elements:
            settings[htrough_element] = {
                "element create": ("from", TTK_CLAM),
            }
            settings[hpbar_element] = {
                "element create": ("from", TTK_DEFAULT),
            }
            self.existing_elements[htrough_element] = True

        settings[h_ttkstyle] = {
            "configure": {
                "thickness": thickness,
                "borderwidth": 1,
                "bordercolor": bordercolor,
                "lightcolor": self.colors.border,
                "pbarrelief": tk.FLAT,
                "troughcolor": troughcolor,
                "background": background,
                "foreground": foreground,
            },
            "layout": [
                (
                    htrough_element,
                    {
                        "sticky": "nswe",
                        "children": [
                            (hpbar_element, {"side": "left", "sticky": "ns"})
                        ],
                    },
                )
            ],
        }
        if has_tk_version_9:
            children = settings[h_ttkstyle]["layout"][0][1]["children"]
            pbar_text = (hpbar_text_element, {"side": "left", "sticky": ""})
            children.append(pbar_text)

        # vertical progressbar
        v_element = v_ttkstyle.replace(".TP", ".P")
        vtrough_element = f"{v_element}.trough"
        vpbar_element = f"{v_element}.pbar"
        # vpbar_text_element = f"{v_element}.ctext"
        if vtrough_element not in self.existing_elements:
            settings[vtrough_element] = {
                "element create": ("from", TTK_CLAM),
            }
            settings[vpbar_element] = {
                "element create": ("from", TTK_DEFAULT),
            }
            self.existing_elements[vtrough_element] = True

        settings[v_ttkstyle] = {
            "configure": {
                "thickness": thickness,
                "borderwidth": 1,
                "bordercolor": bordercolor,
                "lightcolor": self.colors.border,
                "pbarrelief": tk.FLAT,
                "troughcolor": troughcolor,
                "background": background,
            },
            "layout": [
                (
                    vtrough_element,
                    {
                        "sticky": "nswe",
                        "children": [
                            (vpbar_element, {"side": "bottom", "sticky": "we"})
                        ],
                    },
                )
            ],
        }
        # if has_tk_version_9:
        #     children = settings[h_ttkstyle]["layout"][0][1]["children"]
        #     pbar_text = (vpbar_text_element, {"side": "top", "sticky": ""})
        #     children.append(pbar_text)
        if colorname:
            self._register_style(h_ttkstyle)
            self._register_style(v_ttkstyle)

    def create_scale_style(self, settings, colorname=None):
        """Create a style for the ttk.Scale widget."""
        STYLE = "TScale"

        if any([colorname is None, not colorname]):
            h_ttkstyle = f"Horizontal.{STYLE}"
            v_ttkstyle = f"Vertical.{STYLE}"
        else:
            h_ttkstyle = f"{colorname}.Horizontal.{STYLE}"
            v_ttkstyle = f"{colorname}.Vertical.{STYLE}"

        # ( normal, pressed, hover, disabled, htrack, vtrack )
        images = self.assets.create_scale_assets(colorname)

        # horizontal scale
        h_element = h_ttkstyle.replace(".TS", ".S")

        settings[f"{h_element}.slider"] = {
            "element create": (
                "image",
                images[0],
                ("disabled", images[3]),
                ("pressed", images[1]),
                ("hover", images[2]),
            ),
        }
        settings[f"{h_element}.track"] = {
            "element create": (
                "image",
                images[4],
            )
        }
        settings[h_ttkstyle] = {
            "layout": [
                (
                    f"{h_element}.focus",
                    {
                        "expand": "1",
                        "sticky": tk.NSEW,
                        "children": [
                            (f"{h_element}.track", {"sticky": tk.EW}),
                            (
                                f"{h_element}.slider",
                                {"side": tk.LEFT, "sticky": ""},
                            ),
                        ],
                    },
                )
            ],
        }
        # vertical scale
        v_element = v_ttkstyle.replace(".TS", ".S")
        settings[f"{v_element}.slider"] = {
            "element create": (
                "image",
                images[0],
                ("disabled", images[3]),
                ("pressed", images[1]),
                ("hover", images[2]),
            ),
        }
        settings[f"{v_element}.track"] = {
            "element create": (
                "image",
                images[5],
            )
        }
        settings[v_ttkstyle] = {
            "layout": [
                (
                    f"{v_element}.focus",
                    {
                        "expand": "1",
                        "sticky": tk.NSEW,
                        "children": [
                            (f"{v_element}.track", {"sticky": tk.NS}),
                            (
                                f"{v_element}.slider",
                                {"side": tk.TOP, "sticky": ""},
                            ),
                        ],
                    },
                )
            ],
        }
        if colorname:
            self._register_style(h_ttkstyle)
            self._register_style(v_ttkstyle)

    def create_scrollbar_style(self, settings, colorname=None):
        """Create a standard style for the ttk.Scrollbar widget."""
        STYLE = "TScrollbar"

        if any([colorname is None, not colorname]):
            h_ttkstyle = f"Horizontal.{STYLE}"
            v_ttkstyle = f"Vertical.{STYLE}"

            if self.is_light_theme:
                background = self.colors.border
            else:
                background = self.colors.selectbg

        else:
            h_ttkstyle = f"{colorname}.Horizontal.{STYLE}"
            v_ttkstyle = f"{colorname}.Vertical.{STYLE}"
            background = self.colors.get_color(colorname)

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
            else:
                troughcolor = self.colors.light
        else:
            troughcolor = self.colorutil.update_hsv(
                self.colors.selectbg, vd=-0.2
            )

        pressed = self.colorutil.update_hsv(background, vd=-0.05)
        active = self.colorutil.update_hsv(background, vd=0.05)

        scroll_images = self.assets.create_scrollbar_assets(
            background, pressed, active
        )

        # horizontal scrollbar
        settings[f"{h_ttkstyle}.thumb"] = {
            "element create": (
                "image",
                scroll_images[0],
                ("pressed", scroll_images[1]),
                ("active", scroll_images[2]),
                {"border": (3, 0), "sticky": tk.NSEW},
            )
        }
        settings[h_ttkstyle] = {
            "configure": {
                "troughcolor": troughcolor,
                "darkcolor": troughcolor,
                "bordercolor": troughcolor,
                "lightcolor": troughcolor,
                "arrowcolor": background,
                "arrowsize": self.scale_size(11),
                "background": troughcolor,
                "relief": tk.FLAT,
                "borderwidth": 0,
                "arrowcolor": background,
            },
            "map": {
                "arrowcolor": [("pressed", pressed), ("active", active)],
            },
            "layout": [
                (
                    "Horizontal.Scrollbar.trough",
                    {
                        "sticky": "we",
                        "children": [
                            (
                                "Horizontal.Scrollbar.leftarrow",
                                {"side": "left", "sticky": ""},
                            ),
                            (
                                "Horizontal.Scrollbar.rightarrow",
                                {"side": "right", "sticky": ""},
                            ),
                            (
                                f"{h_ttkstyle}.thumb",
                                {"expand": "1", "sticky": "nswe"},
                            ),
                        ],
                    },
                )
            ],
        }

        # vertical scrollbar
        settings[f"{v_ttkstyle}.thumb"] = {
            "element create": (
                "image",
                scroll_images[3],
                ("pressed", scroll_images[4]),
                ("active", scroll_images[5]),
                {"border": (0, 3), "sticky": tk.NSEW},
            )
        }
        settings[v_ttkstyle] = {
            "configure": {
                "troughcolor": troughcolor,
                "darkcolor": troughcolor,
                "bordercolor": troughcolor,
                "lightcolor": troughcolor,
                "arrowcolor": background,
                "arrowsize": self.scale_size(11),
                "background": troughcolor,
                "relief": tk.FLAT,
                "borderwidth": 0,
                "arrowcolor": background,
            },
            "map": {
                "arrowcolor": [("pressed", pressed), ("active", active)],
            },
            "layout": [
                (
                    "Vertical.Scrollbar.trough",
                    {
                        "sticky": "ns",
                        "children": [
                            (
                                "Vertical.Scrollbar.uparrow",
                                {"side": "top", "sticky": ""},
                            ),
                            (
                                "Vertical.Scrollbar.downarrow",
                                {"side": "bottom", "sticky": ""},
                            ),
                            (
                                f"{v_ttkstyle}.thumb",
                                {"expand": "1", "sticky": "nswe"},
                            ),
                        ],
                    },
                )
            ],
        }
        if colorname:
            self._register_style(h_ttkstyle)
            self._register_style(v_ttkstyle)

    def create_spinbox_style(self, settings, colorname=None):
        """Create a style for the ttk.Spinbox widget."""
        STYLE = "TSpinbox"

        if self.is_light_theme:
            disabled_fg = self.colors.border
            bordercolor = self.colors.border
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        if any([colorname is None, not colorname]):
            ttkstyle = STYLE
            focuscolor = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            focuscolor = self.colors.get_color(colorname)

        if all([colorname, colorname is not None]):
            bordercolor = focuscolor

        if colorname == "light":
            arrowfocus = self.colors.fg
        else:
            arrowfocus = focuscolor

        element = ttkstyle.replace(".TS", ".S")
        settings[f"{element}.uparrow"] = {
            "element create": ("from", TTK_DEFAULT),
        }
        settings[f"{element}.downarrow"] = {
            "element create": ("from", TTK_DEFAULT),
        }
        settings[ttkstyle] = {
            "configure": {
                "bordercolor": bordercolor,
                "darkcolor": self.colors.inputbg,
                "lightcolor": self.colors.inputbg,
                "fieldbackground": self.colors.inputbg,
                "foreground": self.colors.inputfg,
                "borderwidth": 0,
                "background": self.colors.inputbg,
                "relief": tk.FLAT,
                "arrowcolor": self.colors.inputfg,
                "insertcolor": self.colors.inputfg,
                "arrowsize": self.scale_size(12),
                "padding": (10, 5),
            },
            "map": {
                "foreground": [("disabled", disabled_fg)],
                "fieldbackground": [("readonly", readonly)],
                "background": [("readonly", readonly)],
                "lightcolor": [
                    ("focus invalid", self.colors.danger),
                    ("focus !disabled", focuscolor),
                    ("readonly", readonly),
                ],
                "darkcolor": [
                    ("focus invalid", self.colors.danger),
                    ("focus !disabled", focuscolor),
                    ("readonly", readonly),
                ],
                "bordercolor": [
                    ("invalid", self.colors.danger),
                    ("focus !disabled", focuscolor),
                    ("hover !disabled", focuscolor),
                ],
                "arrowcolor": [
                    ("disabled !disabled", disabled_fg),
                    ("pressed !disabled", arrowfocus),
                    ("hover !disabled", arrowfocus),
                ],
            },
            "layout": [
                (
                    f"{element}.field",
                    {
                        "side": tk.TOP,
                        "sticky": tk.EW,
                        "children": [
                            (
                                "null",
                                {
                                    "side": tk.RIGHT,
                                    "sticky": "",
                                    "children": [
                                        (
                                            f"{element}.uparrow",
                                            {"side": tk.TOP, "sticky": tk.E},
                                        ),
                                        (
                                            f"{element}.downarrow",
                                            {
                                                "side": tk.BOTTOM,
                                                "sticky": tk.E,
                                            },
                                        ),
                                    ],
                                },
                            ),
                            (
                                f"{element}.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            f"{element}.textarea",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                },
                            ),
                        ],
                    },
                )
            ],
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_treeview_style(self, settings, colorname=None):
        """Create a style for the ttk.Treeview widget."""
        STYLE = "Treeview"

        f = font.nametofont("TkDefaultFont")
        rowheight = f.metrics()["linespace"]

        if self.is_light_theme:
            disabled_fg = self.colorutil.update_hsv(
                self.colors.inputbg, vd=-0.2
            )
            bordercolor = self.colors.border
        else:
            disabled_fg = self.colorutil.update_hsv(
                self.colors.inputbg, vd=-0.3
            )
            bordercolor = self.colors.selectbg

        if any([colorname is None, not colorname]):
            background = self.colors.inputbg
            foreground = self.colors.inputfg
            body_style = STYLE
            header_style = f"{STYLE}.Heading"
            focuscolor = self.colors.primary
        elif colorname == LIGHT and self.is_light_theme:
            background = self.colors.get_color(colorname)
            foreground = self.colors.fg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            focuscolor = background
            bordercolor = focuscolor
        else:
            background = self.colors.get_color(colorname)
            foreground = self.colors.selectfg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            focuscolor = background
            bordercolor = focuscolor

        # treeview header
        settings[header_style] = {
            "configure": {
                "background": background,
                "foreground": foreground,
                "relief": tk.FLAT,
                "padding": 5,
            },
            "map": {
                "foreground": [("disabled", disabled_fg)],
                "bordercolor": [("focus !disabled", background)],
            },
        }
        # treeview body
        settings[body_style] = {
            "configure": {
                "background": self.colors.inputbg,
                "fieldbackground": self.colors.inputbg,
                "foreground": self.colors.inputfg,
                "bordercolor": bordercolor,
                "lightcolor": self.colors.inputbg,
                "darkcolor": self.colors.inputbg,
                "borderwidth": 2,
                "padding": 0,
                "rowheight": rowheight,
                "relief": tk.RAISED,
            },
            "map": {
                "background": [("selected", self.colors.selectbg)],
                "foreground": [
                    ("disabled", disabled_fg),
                    ("selected", self.colors.selectfg),
                ],
                "bordercolor": [
                    ("disabled", bordercolor),
                    ("focus", focuscolor),
                    ("pressed", focuscolor),
                    ("hover", focuscolor),
                ],
                "lightcolor": [("focus", focuscolor)],
                "darkcolor": [("focus", focuscolor)],
            },
            "layout": [
                (
                    "Button.border",
                    {
                        "sticky": tk.NSEW,
                        "border": "1",
                        "children": [
                            (
                                "Treeview.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            "Treeview.treearea",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        }
        # try:
        # self.style.element_create("Treeitem.indicator", "from", TTK_ALT)
        # except:
        # pass
        settings["Treeitem.indicator"] = {
            "element create": ("from", TTK_ALT),
        }
        if colorname:
            self._register_style(body_style)

    def create_radiobutton_style(self, settings, colorname=None):
        """Create a style for the ttk.Radiobutton widget."""

        STYLE = "TRadiobutton"

        disabled_fg = self.colorutil.make_transparent(
            0.30, self.colors.fg, self.colors.bg
        )

        if any([colorname is None, not colorname]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        # ( off, on, disabled )
        images = self.assets.create_radiobutton_assets(colorname)
        width = self.scale_size(20)
        borderpad = self.scale_size(4)

        settings[f"{ttkstyle}.indicator"] = {
            "element create": (
                "image",
                images[1],
                ("disabled selected", images[3]),
                ("disabled", images[2]),
                ("!selected", images[0]),
                {
                    "width": width,
                    "border": borderpad,
                    "sticky": tk.W,
                },
            )
        }

        settings[ttkstyle] = {
            "map": {"foreground": [("disabled", disabled_fg)]},
            "layout": [
                (
                    "Radiobutton.padding",
                    {
                        "children": [
                            (
                                f"{ttkstyle}.indicator",
                                {"side": tk.LEFT, "sticky": ""},
                            ),
                            (
                                "Radiobutton.focus",
                                {
                                    "children": [
                                        (
                                            "Radiobutton.label",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                    "side": tk.LEFT,
                                    "sticky": "",
                                },
                            ),
                        ],
                        "sticky": tk.NSEW,
                    },
                )
            ],
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_checkbutton_style(self, settings, colorname=None):
        """Create a standard style for the ttk.Checkbutton widget."""
        STYLE = "TCheckbutton"

        disabled_fg = self.colorutil.make_transparent(
            0.3, self.colors.fg, self.colors.bg
        )

        if any([colorname is None, not colorname]):
            colorname = PRIMARY
            ttkstyle = STYLE
        else:
            ttkstyle = f"{colorname}.TCheckbutton"

        # ( off, on, disabled )
        images = self.assets.create_checkbutton_assets(colorname)

        element = ttkstyle.replace(".TC", ".C")
        width = self.scale_size(20)
        borderpad = self.scale_size(4)

        settings[f"{element}.indicator"] = {
            "element create": (
                "image",
                images[1],
                ("disabled selected", images[4]),
                ("disabled alternate", images[5]),
                ("disabled", images[2]),
                ("alternate", images[3]),
                ("!selected", images[0]),
                {
                    "width": width,
                    "border": borderpad,
                    "sticky": tk.W,
                },
            )
        }
        settings[ttkstyle] = {
            "configure": {"foreground": self.colors.fg},
            "map": {"foreground": [("disabled", disabled_fg)]},
            "layout": [
                (
                    "Checkbutton.padding",
                    {
                        "children": [
                            (
                                f"{element}.indicator",
                                {"side": tk.LEFT, "sticky": ""},
                            ),
                            (
                                "Checkbutton.focus",
                                {
                                    "children": [
                                        (
                                            "Checkbutton.label",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                    "side": tk.LEFT,
                                    "sticky": "",
                                },
                            ),
                        ],
                        "sticky": tk.NSEW,
                    },
                )
            ],
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_sizegrip_style(self, settings, colorname=None):
        """Create a style for the ttk.Sizegrip widget."""
        STYLE = "TSizegrip"

        if any([colorname is None, not colorname]):
            ttkstyle = STYLE

            if self.is_light_theme:
                grip_color = self.colors.border
            else:
                grip_color = self.colors.inputbg
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            grip_color = self.colors.get_color(colorname)

        image = self.assets.create_sizegrip_assets(grip_color)

        settings[f"{ttkstyle}.Sizegrip.sizegrip"] = {
            "element create": ("image", image)
        }
        settings[ttkstyle] = {
            "layout": [
                (
                    f"{ttkstyle}.Sizegrip.sizegrip",
                    {"side": tk.BOTTOM, "sticky": tk.SE},
                )
            ],
        }
        if colorname:
            self._register_style(ttkstyle)

    def create_striped_progressbar_style(self, settings, colorname=None):
        """Create a striped style for the ttk.Progressbar widget.

        Parameters:

            colorname (str):
                The primary widget color label.
        """
        HSTYLE = "Striped.Horizontal.TProgressbar"
        VSTYLE = "Striped.Vertical.TProgressbar"

        thickness = self.scale_size(12)

        if any([colorname is None, colorname == ""]):
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
        else:
            h_ttkstyle = f"{colorname}.{HSTYLE}"
            v_ttkstyle = f"{colorname}.{VSTYLE}"

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
                bordercolor = self.colors.light
            else:
                troughcolor = self.colors.light
                bordercolor = troughcolor
        else:
            troughcolor = self.colorutil.update_hsv(
                self.colors.selectbg, vd=-0.2
            )
            bordercolor = troughcolor

        # ( horizontal, vertical )
        images = self.assets.create_striped_progressbar_assets(
            thickness, colorname
        )

        # horizontal progressbar
        h_element = h_ttkstyle.replace(".TP", ".P")
        settings[f"{h_element}.pbar"] = {
            "element create": (
                "image",
                images[0],
                {
                    "width": thickness,
                    "sticky": tk.EW,
                },
            )
        }
        settings[h_ttkstyle] = {
            "configure": {
                "troughcolor": troughcolor,
                "thickness": thickness,
                "bordercolor": bordercolor,
                "borderwidth": 1,
            },
            "layout": [
                (
                    f"{h_element}.trough",
                    {
                        "sticky": tk.NSEW,
                        "children": [
                            (
                                f"{h_element}.pbar",
                                {"side": tk.LEFT, "sticky": tk.NS},
                            )
                        ],
                    },
                )
            ],
        }

        # vertical progressbar
        v_element = v_ttkstyle.replace(".TP", ".P")
        settings[f"{v_element}.pbar"] = {
            "element create": (
                "image",
                images[1],
                {
                    "width": thickness,
                    "sticky": tk.NS,
                },
            )
        }
        settings[v_ttkstyle] = {
            "configure": {
                "troughcolor": troughcolor,
                "thickness": thickness,
                "bordercolor": bordercolor,
                "borderwidth": 1,
            },
            "layout": [
                (
                    f"{v_element}.trough",
                    {
                        "sticky": tk.NSEW,
                        "children": [
                            (
                                f"{v_element}.pbar",
                                {"side": tk.BOTTOM, "sticky": tk.EW},
                            )
                        ],
                    },
                )
            ],
        }
        self._register_style(h_ttkstyle)
        self._register_style(v_ttkstyle)

    def create_square_toggle_style(self, settings, colorname=None):
        """Create a square toggle style for the ttk.Checkbutton widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """

        STYLE = "Square.Toggle"

        disabled_fg = self.colorutil.make_transparent(
            0.30, self.colors.fg, self.colors.bg
        )

        if any([colorname is None, colorname == ""]):
            ttkstyle = STYLE
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        # ( off, on, disabled )
        images = self.assets.create_square_toggle_assets(colorname)

        width = self.scale_size(28)
        borderpad = self.scale_size(4)

        settings[f"{ttkstyle}.indicator"] = {
            "element create": (
                "image",
                images[1],
                ("disabled selected", images[3]),
                ("disabled", images[2]),
                ("!selected", images[0]),
                {
                    "width": width,
                    "sticky": tk.W,
                    "border": borderpad,
                },
            )
        }
        settings[ttkstyle] = {
            "configure": {
                "relief": tk.FLAT,
                "borderwidth": 0,
                "foreground": self.colors.fg,
            },
            "layout": [
                (
                    "Toolbutton.border",
                    {
                        "sticky": tk.NSEW,
                        "children": [
                            (
                                "Toolbutton.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            f"{ttkstyle}.indicator",
                                            {"side": tk.LEFT},
                                        ),
                                        (
                                            "Toolbutton.label",
                                            {"side": tk.LEFT},
                                        ),
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
            "map": {
                "foreground": [("disabled", disabled_fg)],
                "background": [
                    ("selected", self.colors.bg),
                    ("!selected", self.colors.bg),
                ],
            },
        }
        self._register_style(ttkstyle)

    def create_round_toggle_style(self, settings, colorname=None):
        """Create a round toggle style for the ttk.Checkbutton widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Round.Toggle"

        disabled_fg = self.colorutil.make_transparent(
            0.30, self.colors.fg, self.colors.bg
        )

        if any([colorname is None, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        # ( off, on, disabled )
        images = self.assets.create_round_toggle_assets(colorname)

        indicator_element = f"{ttkstyle}.indicator"
        if indicator_element not in self.existing_elements:
            width = self.scale_size(28)
            borderpad = self.scale_size(4)

            settings[indicator_element] = {
                "element create": (
                    "image",
                    images[1],
                    ("disabled selected", images[3]),
                    ("disabled", images[2]),
                    ("!selected", images[0]),
                    {
                        "width": width,
                        "sticky": tk.W,
                        "border": borderpad,
                    },
                )
            }
            self.existing_elements[indicator_element] = True

        settings[ttkstyle] = {
            "configure": {
                "relief": tk.FLAT,
                "borderwidth": 0,
                "padding": 0,
                "foreground": self.colors.fg,
                "background": self.colors.bg,
            },
            "map": {
                "foreground": [("disabled", disabled_fg)],
                "background": [("selected", self.colors.bg)],
            },
            "layout": [
                (
                    "Toolbutton.border",
                    {
                        "sticky": tk.NSEW,
                        "children": [
                            (
                                "Toolbutton.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            f"{ttkstyle}.indicator",
                                            {"side": tk.LEFT},
                                        ),
                                        (
                                            "Toolbutton.label",
                                            {"side": tk.LEFT},
                                        ),
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        }
        self._register_style(ttkstyle)

    def create_round_scrollbar_style(self, settings, colorname=None):
        """Create a round style for the ttk.Scrollbar widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TScrollbar"

        if any([colorname is None, colorname == ""]):
            h_ttkstyle = f"Round.Horizontal.{STYLE}"
            v_ttkstyle = f"Round.Vertical.{STYLE}"

            if self.is_light_theme:
                background = self.colors.border
            else:
                background = self.colors.selectbg

        else:
            h_ttkstyle = f"{colorname}.Round.Horizontal.{STYLE}"
            v_ttkstyle = f"{colorname}.Round.Vertical.{STYLE}"
            background = self.colors.get_color(colorname)

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
            else:
                troughcolor = self.colors.light
        else:
            troughcolor = self.colorutil.update_hsv(
                self.colors.selectbg, vd=-0.2
            )

        pressed = self.colorutil.update_hsv(background, vd=-0.05)
        active = self.colorutil.update_hsv(background, vd=0.05)

        scroll_images = self.assets.create_round_scrollbar_assets(
            background, pressed, active
        )

        # horizontal scrollbar
        settings[f"{h_ttkstyle}.thumb"] = {
            "element create": (
                "image",
                scroll_images[0],
                ("pressed", scroll_images[1]),
                ("active", scroll_images[2]),
                {
                    "padding": 0,
                    "sticky": tk.EW,
                    "border": self.scale_size(9),
                },
            )
        }
        settings[h_ttkstyle] = {
            "configure": {
                "troughcolor": troughcolor,
                "darkcolor": troughcolor,
                "bordercolor": troughcolor,
                "lightcolor": troughcolor,
                "arrowcolor": background,
                "arrowsize": self.scale_size(11),
                "background": troughcolor,
                "relief": tk.FLAT,
                "borderwidth": 0,
            },
            "layout": [
                (
                    "Horizontal.Scrollbar.trough",
                    {
                        "sticky": "we",
                        "children": [
                            (
                                "Horizontal.Scrollbar.leftarrow",
                                {"side": "left", "sticky": ""},
                            ),
                            (
                                "Horizontal.Scrollbar.rightarrow",
                                {"side": "right", "sticky": ""},
                            ),
                            (
                                f"{h_ttkstyle}.thumb",
                                {"expand": "1", "sticky": "nswe"},
                            ),
                        ],
                    },
                )
            ],
            "map": {"arrowcolor": [("pressed", pressed), ("active", active)]},
        }

        # vertical scrollbar
        settings[f"{v_ttkstyle}.thumb"] = {
            "element create": (
                "image",
                scroll_images[3],
                ("pressed", scroll_images[4]),
                ("active", scroll_images[5]),
                {
                    "padding": 0,
                    "sticky": tk.NS,
                    "border": self.scale_size(9),
                },
            )
        }
        settings[v_ttkstyle] = {
            "configure": {
                "troughcolor": troughcolor,
                "darkcolor": troughcolor,
                "bordercolor": troughcolor,
                "lightcolor": troughcolor,
                "arrowcolor": background,
                "arrowsize": self.scale_size(11),
                "background": troughcolor,
                "relief": tk.FLAT,
                # "borderwidth": 0,
            },
            "layout": [
                (
                    "Vertical.Scrollbar.trough",
                    {
                        "sticky": "ns",
                        "children": [
                            (
                                "Vertical.Scrollbar.uparrow",
                                {"side": "top", "sticky": ""},
                            ),
                            (
                                "Vertical.Scrollbar.downarrow",
                                {"side": "bottom", "sticky": ""},
                            ),
                            (
                                f"{v_ttkstyle}.thumb",
                                {"expand": "1", "sticky": "nswe"},
                            ),
                        ],
                    },
                )
            ],
            "map": {"arrowcolor": [("pressed", pressed), ("active", active)]},
        }
        if colorname:
            self._register_style(h_ttkstyle)
            self._register_style(v_ttkstyle)

    def create_table_treeview_style(self, settings, colorname=None):
        """Create a style for the Tableview widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Table.Treeview"

        f = font.nametofont("TkDefaultFont")
        rowheight = f.metrics()["linespace"]

        if self.is_light_theme:
            disabled_fg = self.colorutil.update_hsv(
                self.colors.inputbg, vd=-0.2
            )
            bordercolor = self.colors.border
            hover = self.colorutil.update_hsv(self.colors.light, vd=-0.1)
        else:
            disabled_fg = self.colorutil.update_hsv(
                self.colors.inputbg, vd=-0.3
            )
            bordercolor = self.colors.selectbg
            hover = self.colorutil.update_hsv(self.colors.dark, vd=0.1)

        if any([colorname is None, colorname == ""]):
            background = self.colors.inputbg
            foreground = self.colors.inputfg
            body_style = STYLE
            header_style = f"{STYLE}.Heading"
        elif colorname == LIGHT and self.is_light_theme:
            background = self.colors.get_color(colorname)
            foreground = self.colors.fg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            hover = self.colorutil.update_hsv(background, vd=-0.1)
        else:
            background = self.colors.get_color(colorname)
            foreground = self.colors.selectfg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            hover = self.colorutil.update_hsv(background, vd=0.1)

        # treeview header
        settings[header_style] = {
            "configure": {
                "background": background,
                "foreground": foreground,
                "relief": tk.RAISED,
                "borderwidth": 1,
                "darkcolor": background,
                "bordercolor": bordercolor,
                "lightcolor": background,
                "padding": 5,
            },
            "map": {
                "foreground": [("disabled", disabled_fg)],
                "background": [
                    ("active !disabled", hover),
                ],
                "darkcolor": [
                    ("active !disabled", hover),
                ],
                "lightcolor": [
                    ("active !disabled", hover),
                ],
            },
        }

        settings[body_style] = {
            "configure": {
                "background": self.colors.inputbg,
                "fieldbackground": self.colors.inputbg,
                "foreground": self.colors.inputfg,
                "bordercolor": bordercolor,
                "lightcolor": self.colors.inputbg,
                "darkcolor": self.colors.inputbg,
                "borderwidth": 2,
                "padding": 0,
                "rowheight": rowheight,
                "relief": tk.RAISED,
            },
            "map": {
                "background": [("selected", self.colors.selectbg)],
                "foreground": [
                    ("disabled", disabled_fg),
                    ("selected", self.colors.selectfg),
                ],
            },
            "layout": [
                (
                    "Button.border",
                    {
                        "sticky": tk.NSEW,
                        "border": "1",
                        "children": [
                            (
                                "Treeview.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            "Treeview.treearea",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        }
        self._register_style(body_style)

    def create_floodgauge_style(self, settings, colorname=None):
        """Create a ttk style for the pygubu Floodgauge
        widget. This is a custom widget style that uses components of
        the progressbar and label.
        """
        HSTYLE = "Horizontal.TFloodgauge"
        VSTYLE = "Vertical.TFloodgauge"
        FLOOD_FONT = "-size 14"

        if any([colorname is None, colorname == ""]):
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
            background = self.colors.primary
        else:
            h_ttkstyle = f"{colorname}.{HSTYLE}"
            v_ttkstyle = f"{colorname}.{VSTYLE}"
            background = self.colors.get_color(colorname)

        if colorname == LIGHT:
            foreground = self.colors.fg
            troughcolor = self.colors.bg
        else:
            troughcolor = self.colorutil.update_hsv(background, sd=-0.3, vd=0.8)
            foreground = self.colors.selectfg

        # horizontal floodgauge
        h_element = h_ttkstyle.replace(".TF", ".F")
        # vertical floodgauge
        v_element = v_ttkstyle.replace(".TF", ".F")

        ttk_elements = (
            (f"{h_element}.trough", TTK_CLAM),
            (f"{h_element}.pbar", TTK_DEFAULT),
            (f"{v_element}.trough", TTK_CLAM),
            (f"{v_element}.pbar", TTK_DEFAULT),
        )
        for element_name, from_ in ttk_elements:
            settings[element_name] = {
                "element create": ("from", from_),
            }

        h_layout = None
        v_layout = None
        if tk.TkVersion >= 9:
            h_layout, v_layout = self.floodgauge_layout_tk9(
                h_element, v_element
            )
        else:
            h_layout, v_layout = self.floodgauge_layout_tk8(
                h_element, v_element
            )

        settings[h_ttkstyle] = {
            "configure": dict(
                thickness=50,
                borderwidth=1,
                bordercolor=background,
                lightcolor=background,
                pbarrelief=tk.FLAT,
                troughcolor=troughcolor,
                background=background,
                foreground=foreground,
                justify=tk.CENTER,
                anchor=tk.CENTER,
                font=FLOOD_FONT,
            ),
            "layout": h_layout,
        }
        settings[v_ttkstyle] = {
            "configure": dict(
                thickness=50,
                borderwidth=1,
                bordercolor=background,
                lightcolor=background,
                pbarrelief=tk.FLAT,
                troughcolor=troughcolor,
                background=background,
                foreground=foreground,
                justify=tk.CENTER,
                anchor=tk.CENTER,
                font=FLOOD_FONT,
            ),
            "layout": v_layout,
        }

        if colorname:
            self._register_style(h_ttkstyle)
            self._register_style(v_ttkstyle)

    def floodgauge_layout_tk9(self, h_element: str, v_element: str) -> tuple:
        h_layout = [
            (
                f"{h_element}.trough",
                {
                    "children": [
                        (f"{h_element}.pbar", {"side": "left", "sticky": "ns"}),
                        (
                            f"{h_element}.ctext",
                            # {"side": "left", "sticky": ""}
                            {"side": "left", "sticky": "", "expand": True},
                        ),
                    ],
                    "sticky": "nswe",
                },
            )
        ]

        v_layout = [
            (
                f"{v_element}.trough",
                {
                    "children": [
                        (
                            f"{v_element}.pbar",
                            {"side": "bottom", "sticky": "we"},
                        ),
                        (f"{v_element}.ctext", {"sticky": "", "expand": True}),
                    ],
                    "sticky": "nswe",
                },
            )
        ]
        return h_layout, v_layout

    def floodgauge_layout_tk8(self, h_element: str, v_element: str) -> tuple:
        TKCLASS_NAME = "Floodgauge"
        h_layout = [
            (
                f"{h_element}.trough",
                {
                    "children": [
                        (
                            f"{h_element}.pbar",
                            {"sticky": "ns"},
                        ),
                        (f"{TKCLASS_NAME}.label", {"sticky": ""}),
                    ],
                    "sticky": "nsew",
                },
            )
        ]
        v_layout = [
            (
                f"{v_element}.trough",
                {
                    "children": [
                        (
                            f"{v_element}.pbar",
                            {"sticky": "ew"},
                        ),
                        (f"{TKCLASS_NAME}.label", {"sticky": ""}),
                    ],
                    "sticky": "nsew",
                },
            )
        ]
        return h_layout, v_layout
