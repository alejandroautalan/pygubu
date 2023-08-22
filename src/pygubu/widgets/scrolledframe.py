# encoding: utf-8
import tkinter as tk
import tkinter.ttk as ttk

from pygubu.binding import (
    ApplicationLevelBindManager as BindManager,
    remove_binding,
)
from .tkscrolledframe import ScrolledFrameBase


class ScrolledFrame(ScrolledFrameBase, ttk.Frame):
    _framecls = ttk.Frame
    _sbarcls = ttk.Scrollbar
