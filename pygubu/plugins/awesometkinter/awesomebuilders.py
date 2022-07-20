"""
Documentation, License etc.

@package pygubu.plugins.awesometkinter
"""
import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import BuilderObject, register_widget
from pygubu.plugins.tk.tkstdwidgets import TKFrame, TKCheckbutton
from pygubu.plugins.ttk.ttkstdwidgets import TTKButton, TTKFrame, TTKRadiobutton
import awesometkinter as atk

designer_tab_label = "AwesomeTkinter"
module_uid = "awesometkinter"


class ATKInitializeMixin:
    def atk_initialize(self, master):
        root = master
        if not isinstance(master, tk.Toplevel) or not isinstance(master, tk.Tk):
            root = master.winfo_toplevel()
        root.config(background=atk.DEFAULT_COLOR)


class Frame3dBO(TTKFrame, ATKInitializeMixin):
    class_ = atk.Frame3d

    def realize(self, parent):
        self.atk_initialize(parent.get_child_master())
        super(Frame3dBO, self).realize(parent)


_builder_uid = module_uid + ".frame3d"
register_widget(_builder_uid, Frame3dBO, "Frame3d", ("ttk", designer_tab_label))


class ScrollableFrameBO(TKFrame, ATKInitializeMixin):
    class_ = atk.ScrollableFrame

    def realize(self, parent):
        self.atk_initialize(parent.get_child_master())
        super(ScrollableFrameBO, self).realize(parent)

    def _get_init_args(self):
        # this widget does not support class_ wk argument
        args = super(ScrollableFrameBO, self)._get_init_args()
        args.pop("class_", None)
        return args


_builder_uid = module_uid + ".scrollable_frame"
register_widget(
    _builder_uid,
    ScrollableFrameBO,
    "ScrollableFrame",
    ("ttk", designer_tab_label),
)


class Button3dBO(TTKButton):
    class_ = atk.Button3d


_builder_uid = module_uid + ".button3d"
register_widget(
    _builder_uid, Button3dBO, "Button3d", ("ttk", designer_tab_label)
)


class RadiobuttonBO(TTKRadiobutton):
    class_ = atk.Radiobutton


_builder_uid = module_uid + ".radiobutton"
register_widget(
    _builder_uid, RadiobuttonBO, "Radiobutton", ("ttk", designer_tab_label)
)


class CheckbuttonBO(TKCheckbutton):
    class_ = atk.Checkbutton


_builder_uid = module_uid + ".checkbutton"
register_widget(
    _builder_uid, CheckbuttonBO, "Checkbutton", ("ttk", designer_tab_label)
)


class RadialProgressbarBO(BuilderObject):
    class_ = atk.RadialProgressbar


_builder_uid = module_uid + ".radialprogressbar"
register_widget(
    _builder_uid,
    RadialProgressbarBO,
    "RadialProgressbar",
    ("ttk", designer_tab_label),
)


class RadialProgressbar3dBO(BuilderObject):
    class_ = atk.RadialProgressbar3d


_builder_uid = module_uid + ".radialprogressbar3d"
register_widget(
    _builder_uid,
    RadialProgressbar3dBO,
    "RadialProgressbar3d",
    ("ttk", designer_tab_label),
)


class SegmentbarBO(BuilderObject):
    class_ = atk.Segmentbar


_builder_uid = module_uid + ".Segmentbar"
register_widget(
    _builder_uid, SegmentbarBO, "Segmentbar", ("ttk", designer_tab_label)
)
