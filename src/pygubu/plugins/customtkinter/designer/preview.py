import tkinter as tk
from customtkinter import CTkFrame, set_appearance_mode
from pygubu.api.v1 import BuilderObject
from pygubu.plugins.pygubu.designer.basehelpers import (
    ToplevelPreviewBaseBO,
    ToplevelPreviewFactory,
    ToplevelPreviewMixin,
)

#
# Preview classes for CTKToplevel
#
CTKToplevelPreview = ToplevelPreviewFactory(
    "CTKToplevelPreview",
    (ToplevelPreviewMixin, CTkFrame, object),
    {},
)


class CTkToplevelPreviewBO(ToplevelPreviewBaseBO):
    class_ = CTKToplevelPreview
    ro_properties = ToplevelPreviewBaseBO.ro_properties + ("background",)


#
# Preview classes for CTK
#
CTKPreview = ToplevelPreviewFactory(
    "CTKPreview",
    (ToplevelPreviewMixin, CTkFrame, object),
    {},
)


class CTkPreviewBO(ToplevelPreviewBaseBO):
    class_ = CTKPreview
    properties = ToplevelPreviewBaseBO.properties + ("appearance_mode",)
    ro_properties = ToplevelPreviewBaseBO.ro_properties + ("background",)

    def _set_property(self, target_widget, pname, value):
        if pname == "appearance_mode":
            set_appearance_mode(value)
        else:
            return super()._set_property(target_widget, pname, value)
