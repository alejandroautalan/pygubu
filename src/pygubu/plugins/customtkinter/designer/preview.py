import tkinter as tk
from customtkinter import CTkFrame
from pygubu.api.v1 import BuilderObject
from pygubu.plugins.pygubu.designer.basehelpers import (
    ToplevelPreviewBaseBO,
    ToplevelPreviewFactory,
    ToplevelPreviewMixin,
)


CTKToplevelPreview = ToplevelPreviewFactory(
    "CTKToplevelPreview",
    (ToplevelPreviewMixin, CTkFrame, object),
    {},
)


class CTkToplevelPreviewBO(ToplevelPreviewBaseBO):
    class_ = CTKToplevelPreview


CTKPreview = ToplevelPreviewFactory(
    "CTKPreview",
    (ToplevelPreviewMixin, CTkFrame, object),
    {},
)


class CTkPreviewBO(ToplevelPreviewBaseBO):
    class_ = CTKPreview
