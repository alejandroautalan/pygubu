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


class ThemedTKinterFramePreviewBO(tkmt_builders.ThemedTkFrameBO):
    layout_required = True
    class_ = ThemedTkFramePreview

    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)
        if "title" not in args:
            args["title"] = self.wmeta.identifier
        return args

    def realize(self, parent, extra_init_args: dict = None):
        return super(tkmt_builders.ThemedTkFrameBO, self).realize(
            parent, extra_init_args
        )

    def get_child_master(self):
        return self.widget.tkmt_widget


class PreviewBaseMixin:
    def realize(self, parent, extra_init_args: dict = None):
        self.tkmt_widget = super().realize(parent, extra_init_args)
        self.widget = tkmt_to_tkwidget(self.tkmt_widget)
        return self.widget

    def get_child_master(self):
        return self.tkmt_widget


class FramePreviewBO(PreviewBaseMixin, tkmt_builders.FrameBO):
    ...


class LabelFramePreviewBO(PreviewBaseMixin, tkmt_builders.LabelFrameBO):
    ...


class NotebookPreviewBO(PreviewBaseMixin, tkmt_builders.NotebookBO):
    ...


class NotebookTabPreviewBO(PreviewBaseMixin, tkmt_builders.NotebookTabBO):
    ...


class PanedWindowPreviewBO(PreviewBaseMixin, tkmt_builders.PanedWindowBO):
    ...


class PanedWindowPanePreviewBO(
    PreviewBaseMixin, tkmt_builders.PanedWindowPaneBO
):
    ...


class FrameNextColPreviewBO(PreviewBaseMixin, tkmt_builders.FrameNextColBO):
    ...
