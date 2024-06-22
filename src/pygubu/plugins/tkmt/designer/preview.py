import tkinter as tk
import tkinter.ttk as ttk

from pygubu.api.v1 import BuilderObject
from TKinterModernThemes.WidgetFrame import WidgetFrame

import pygubu.plugins.tkmt.widgets as tkmt_widgets


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


class ThemedTKinterFramePreviewBO(tkmt_widgets.ThemedTkFrameBO):
    layout_required = True
    class_ = ThemedTkFramePreview

    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)
        if "title" not in args:
            args["title"] = self.wmeta.identifier
        return args

    def realize(self, parent, extra_init_args: dict = None):
        return super(tkmt_widgets.ThemedTkFrameBO, self).realize(
            parent, extra_init_args
        )

    def get_child_master(self):
        return self.widget.tkmt_widget


class PreviewBaseMixin:
    def realize(self, parent, extra_init_args: dict = None):
        self.tkmt_widget = super().realize(parent, extra_init_args)
        self.widget = self.tkmt_widget.master
        return self.widget

    def get_child_master(self):
        return self.tkmt_widget


class wFramePreviewBO(PreviewBaseMixin, tkmt_widgets.wFrameBO):
    ...


class wLabelFramePreviewBO(PreviewBaseMixin, tkmt_widgets.wLabelFrameBO):
    ...
