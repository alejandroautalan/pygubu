import tkinter as tk

from pygubu.api.v1 import BuilderObject, register_widget
from .basehelpers import (
    ToplevelPreviewFactory,
    ToplevelPreviewMixin,
    ToplevelPreviewBaseBO,
)


ToplevelFramePreview = ToplevelPreviewFactory(
    "ToplevelFramePreview",
    (ToplevelPreviewMixin, tk.Frame, object),
    {},
)


class ToplevelFramePreviewBO(ToplevelPreviewBaseBO):
    class_ = ToplevelFramePreview
