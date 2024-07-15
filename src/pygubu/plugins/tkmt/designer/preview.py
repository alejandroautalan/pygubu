import tkinter as tk
import tkinter.ttk as ttk
import pygubu.plugins.tkmt.widgets as tkmt_builders

from TKinterModernThemes.WidgetFrame import WidgetFrame
from ..base import tkmt_to_tkwidget


class ThemedTkFramePreview(ttk.Frame):
    def __init__(
        self,
        master,
        title: str,
        theme: str = "",
        mode: str = "",
        usecommandlineargs=True,
        useconfigfile=True,
    ):
        super().__init__(master, width=200, height=200)
        self.tkmt_widget = WidgetFrame(self, "Master Frame")


class PreviewBaseMixin:
    def realize(self, parent, extra_init_args: dict = None):
        if self.class_ == ThemedTkFramePreview:
            self.widget = super().realize(parent, extra_init_args)
            self.tkmt_widget = self.widget.tkmt_widget
        else:
            self.tkmt_widget = super().realize(parent, extra_init_args)
            self.widget = tkmt_to_tkwidget(self.tkmt_widget)
        return self.widget

    def get_child_master(self):
        return self.tkmt_widget


class ThemedTKinterFramePreviewBO(
    PreviewBaseMixin, tkmt_builders.ThemedTKinterFrameBO
):
    class_ = ThemedTkFramePreview
    layout_required = True
    pos_args = (
        "master",
        "title",
    )
    properties = pos_args + tkmt_builders.ThemedTKinterFrameBO.kw_args

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {"master": master, "title": self.wmeta.identifier}


class FramePreviewBO(PreviewBaseMixin, tkmt_builders.FrameBO):
    ...


class LabelFramePreviewBO(PreviewBaseMixin, tkmt_builders.LabelFrameBO):
    ...


class NotebookPreviewBO(PreviewBaseMixin, tkmt_builders.NotebookBO):
    ...


class NotebookTabPreviewBO(PreviewBaseMixin, tkmt_builders.NotebookTabBO):
    def _set_property(self, target_widget, pname, value):
        return super()._set_property(self.tkmt_widget, pname, value)

    def configure_children(self, target=None):
        super().configure_children(self.tkmt_widget)


class PanedWindowPreviewBO(PreviewBaseMixin, tkmt_builders.PanedWindowBO):
    ...


class PanedWindowPanePreviewBO(
    PreviewBaseMixin, tkmt_builders.PanedWindowPaneBO
):
    ...


class FrameNextColPreviewBO(PreviewBaseMixin, tkmt_builders.FrameNextColBO):
    ...
