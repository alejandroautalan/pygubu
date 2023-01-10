import tkinter as tk
from customtkinter import (
    CTkFrame,
    set_appearance_mode,
    set_default_color_theme,
    CTkTabview,
)
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass
from pygubu.api.v1 import BuilderObject
from pygubu.plugins.pygubu.designer.basehelpers import (
    ToplevelPreviewBaseBO,
    ToplevelPreviewFactory,
    ToplevelPreviewMixin,
)
from ..widgets import CTkFrameBO
from ..tabview import CTkTabviewBO


#
# Preview class for CTkFrame
#
class CTkFrameForPreview(CTkFrame):
    def winfo_children(self):
        # CTkFrame has a hidden canvas inside. So, to make it clickable on preview
        # we need a hack.
        return super(tk.Frame, self).winfo_children()


class CTkFramePreviewBO(CTkFrameBO):
    class_ = CTkFrameForPreview


#
# Preview class for Tabview
#
class CTkTabviewForPreview(CTkTabview):
    #    def winfo_children(self):
    #        return super(tk.Frame, self).winfo_children()

    def bind(self, sequence=None, func=None, add=None):
        return super(tk.Frame, self).bind(sequence, func, add)


class CTkTabviewForPreviewBO(CTkTabviewBO):
    class_ = CTkTabviewForPreview


#
# Preview classes for CTKToplevel
#


class CTKToplevelPreviewMixin:
    def configure(self, cnf=None, **kw):
        if cnf:
            return super().configure(cnf, **kw)
        # configure properties not supported by CtkFrame but yes by CtkToplevel
        props = ("borderwidth", "highlightbackground", "highlightthickness")
        for pname in props:
            if pname in kw:
                super(CTkBaseClass, self).configure(**{pname: kw.pop(pname)})
        return super().configure(cnf, **kw)


CTKToplevelPreview = ToplevelPreviewFactory(
    "CTKToplevelPreview",
    (CTKToplevelPreviewMixin, ToplevelPreviewMixin, CTkFrameForPreview, object),
    {},
)


class CTkToplevelPreviewBO(ToplevelPreviewBaseBO):
    class_ = CTKToplevelPreview
    ro_properties = ToplevelPreviewBaseBO.ro_properties + (
        "background",
        "fg_color",
    )

    def _process_property_value(self, pname, value):
        if pname in ("width", "height"):
            return int(value)
        return super()._process_property_value(pname, value)


#
# Preview classes for CTK
#
class CTKPreviewMixin:
    def configure(self, cnf=None, **kw):
        if cnf:
            return super().configure(cnf, **kw)
        # configure properties not supported by CtkFrame but yes by Ctk
        props = ("padx", "pady", "relief", "takefocus")
        for pname in props:
            if pname in kw:
                super(CTkBaseClass, self).configure(**{pname: kw.pop(pname)})
        return super().configure(cnf, **kw)


CTKPreview = ToplevelPreviewFactory(
    "CTKPreview",
    (CTKPreviewMixin, ToplevelPreviewMixin, CTkFrameForPreview, object),
    {},
)


class CTkPreviewBO(ToplevelPreviewBaseBO):
    class_ = CTKPreview
    properties = ToplevelPreviewBaseBO.properties + ("appearance_mode",)
    ro_properties = ToplevelPreviewBaseBO.ro_properties + ("fg_color",)

    def _set_property(self, target_widget, pname, value):
        if pname == "appearance_mode":
            set_appearance_mode(value)
        elif pname == "color_theme":
            set_default_color_theme(value)
        else:
            return super()._set_property(target_widget, pname, value)
