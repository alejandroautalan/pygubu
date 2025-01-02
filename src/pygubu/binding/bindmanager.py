import logging
import platform
import tkinter as tk

from pygubu.utils.widget import iter_to_toplevel


logger = logging.getLogger(__name__)


class MouseWheelCommand:
    def __init__(self, view_command, factor=1):
        self.view_command = view_command
        self.factor = factor


class UnixMouseWheelCommandTk9(MouseWheelCommand):
    def __call__(self, event=None) -> bool:
        self.view_command(
            "scroll",
            (-1) * int((event.delta / 120) * self.factor),
            "units",
        )
        scroll_rs = self.view_command()
        if scroll_rs is None:
            return False
        can_keep_scrolling = scroll_rs[0] != 0.0
        if event.delta < 0:
            can_keep_scrolling = scroll_rs[1] != 1.0
        return can_keep_scrolling


class UnixMouseWheelCommandTk8(MouseWheelCommand):
    def __call__(self, event=None) -> bool:
        can_keep_scrolling = True
        if event.num == 4:
            self.view_command("scroll", (-1) * self.factor, "units")
            scroll_rs = self.view_command()
            can_keep_scrolling = scroll_rs[0] != 0.0
        elif event.num == 5:
            self.view_command("scroll", self.factor, "units")
            scroll_rs = self.view_command()
            can_keep_scrolling = scroll_rs[1] != 1.0
        return can_keep_scrolling


class WindowsMouseWheelCommand(MouseWheelCommand):
    def __call__(self, event=None) -> bool:
        self.view_command(
            "scroll", (-1) * int((event.delta / 120) * self.factor), "units"
        )
        scroll_rs = self.view_command()
        can_keep_scrolling = scroll_rs[0] != 0.0
        if event.delta < 0:
            can_keep_scrolling = scroll_rs[1] != 1.0
        return can_keep_scrolling


class DarwingMouseWheelCommand(MouseWheelCommand):
    def __call__(self, event=None) -> bool:
        self.view_command("scroll", event.delta, "units")
        scroll_rs = self.view_command()
        can_keep_scrolling = scroll_rs[0] != 0.0
        if event.delta < 0:
            can_keep_scrolling = scroll_rs[1] != 1.0
        return can_keep_scrolling


class UnknownMouseWheelCommand(MouseWheelCommand):
    def __call__(self, event=None) -> bool:
        # Unknown platform scroll method
        return False


class AppBindManagerBase(object):
    # Acces to tk instance
    master: tk.Widget = None
    # Mouse wheel support
    mw_listeners = []  # Mousewheel listeners
    mw_initialized = False

    @classmethod
    def on_mousewheel(cls, event):
        """
        Manage Application level mousewheel event

        Here we expect that the widget in wm_listeners list,
        have a method "on_mousewheel" created with the
        make_onmousewheel_cb function of this class.
        """
        # print("on_mousewheel, cls", event)
        widget_below = event.widget
        if not isinstance(widget_below, tk.Widget):
            try:
                widget_below = cls.master.winfo_containing(
                    event.x_root, event.y_root
                )
            except KeyError:
                widget_below = None
        if widget_below:
            # print("widget:", type(widget_below), widget_below)
            # print("widget_bindings:", widget_below.bind())
            # cname = widget_below.winfo_class()
            # print("class_bindings:", cname, widget_below.bind_class(cname))
            # print("tags:", widget_below.bindtags())
            for w in iter_to_toplevel(widget_below):
                if w in cls.mw_listeners:
                    can_keep_scrolling = w.on_mousewheel(event)
                    if can_keep_scrolling:
                        break

    @classmethod
    def mousewheel_bind(cls, widget):
        if widget not in cls.mw_listeners:
            cls.mw_listeners.append(widget)

    @classmethod
    def mousewheel_unbind(cls, widget):
        if widget in cls.mw_listeners:
            cls.mw_listeners.remove(widget)

    @classmethod
    def init_mousewheel_binding(cls, master):
        if not cls.mw_initialized:
            cls.master = master.winfo_toplevel()
            _os = platform.system()
            if _os in ("Linux", "OpenBSD", "FreeBSD"):
                if tk.TkVersion >= 9:
                    master.bind_all("<MouseWheel>", cls.on_mousewheel, add="+")
                else:
                    master.bind_all("<4>", cls.on_mousewheel, add="+")
                    master.bind_all("<5>", cls.on_mousewheel, add="+")
            else:
                # Windows and MacOS
                master.bind_all(
                    "<MouseWheel>",
                    cls.on_mousewheel,
                    add="+",
                )
            cls.mw_initialized = True

    @classmethod
    def make_onmousewheel_cb(cls, widget, orient, factor=1):
        """Create a callback to manage mousewheel events

        orient: string (posible values: ('x', 'y'))
        widget: widget that implement tk xview and yview methods
        """
        _os = platform.system()
        view_command = getattr(widget, orient + "view")
        on_mousewheel = None
        if _os in ("Linux", "OpenBSD", "FreeBSD"):
            if tk.TkVersion >= 9:
                on_mousewheel = UnixMouseWheelCommandTk9(view_command, factor)
            else:
                on_mousewheel = UnixMouseWheelCommandTk8(view_command, factor)
        elif _os == "Windows":
            on_mousewheel = WindowsMouseWheelCommand(view_command, factor)
        elif _os == "Darwin":
            on_mousewheel = DarwingMouseWheelCommand(view_command, factor)
        else:
            on_mousewheel = UnknownMouseWheelCommand(view_command, factor)

        return on_mousewheel


class ApplicationLevelBindManager(AppBindManagerBase):
    ...
