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
        can_keep_scrolling = False
        self.view_command(
            "scroll",
            (-1) * int((event.delta / 120) * self.factor),
            "units",
        )
        scroll_rs = self.view_command()
        if scroll_rs is not None:
            can_keep_scrolling = scroll_rs[0] != 0.0
            if event.delta < 0:
                can_keep_scrolling = scroll_rs[1] != 1.0
        return can_keep_scrolling


class UnixMouseWheelCommandTk8(MouseWheelCommand):
    def __call__(self, event=None) -> bool:
        can_keep_scrolling = False
        if event.num == 4:
            self.view_command("scroll", (-1) * self.factor, "units")
            scroll_rs = self.view_command()
            if scroll_rs is not None:
                can_keep_scrolling = scroll_rs[0] != 0.0
        elif event.num == 5:
            self.view_command("scroll", self.factor, "units")
            scroll_rs = self.view_command()
            if scroll_rs is not None:
                can_keep_scrolling = scroll_rs[1] != 1.0
        return can_keep_scrolling


class WindowsMouseWheelCommand(MouseWheelCommand):
    def __call__(self, event=None) -> bool:
        can_keep_scrolling = False
        self.view_command(
            "scroll", (-1) * int((event.delta / 120) * self.factor), "units"
        )
        scroll_rs = self.view_command()
        if scroll_rs is not None:
            can_keep_scrolling = scroll_rs[0] != 0.0
            if event.delta < 0:
                can_keep_scrolling = scroll_rs[1] != 1.0
        return can_keep_scrolling


class DarwingMouseWheelCommand(MouseWheelCommand):
    def __call__(self, event=None) -> bool:
        can_keep_scrolling = False
        self.view_command("scroll", event.delta, "units")
        scroll_rs = self.view_command()
        if scroll_rs is not None:
            can_keep_scrolling = scroll_rs[0] != 0.0
            if event.delta < 0:
                can_keep_scrolling = scroll_rs[1] != 1.0
        return can_keep_scrolling


class UnknownMouseWheelCommand(MouseWheelCommand):
    def __call__(self, event=None) -> bool:
        # Unknown platform scroll method
        return False


class AppBindManagerBase(object):
    CLASS_NAME = "TAppBindManager"
    FLAG_NAME = "_appbind_visited"
    # Acces to tk instances
    masters: list[tk.Widget] = []
    # Mouse wheel support
    mw_listeners = []  # Mousewheel listeners

    @classmethod
    def master_for_path(cls, widget_path: str):
        master_found = None
        for master in cls.masters:
            exists = master.tk.eval(f"winfo exists {widget_path}")
            if exists:
                master_found = master
                break
        return master_found

    @classmethod
    def on_mousewheel_enter(cls, event):
        """Prepare widget for future mousewheel event."""
        widget_below = event.widget
        if not isinstance(widget_below, tk.Widget):
            return
        if not hasattr(widget_below, cls.FLAG_NAME):
            flag_value = cls.has_mousewheel_listener(widget_below)
            setattr(widget_below, cls.FLAG_NAME, flag_value)
            if flag_value:
                # print(f"Preparing widget for mousewheel {widget_below}")
                # cname = widget_below.winfo_class()
                tags = list(widget_below.bindtags())
                tags.insert(0, cls.CLASS_NAME)
                widget_below.bindtags(tags)

    @classmethod
    def has_mousewheel_listener(cls, widget: tk.Widget) -> bool:
        for w in iter_to_toplevel(widget):
            if w in cls.mw_listeners:
                return True
        return False

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
                master = cls.master_for_path(widget_below)
                widget_below = master.winfo_containing(
                    event.x_root, event.y_root
                )
            except (AttributeError, KeyError):
                widget_below = None
        # scroll_performed = False
        if widget_below:
            for w in iter_to_toplevel(widget_below):
                if w in cls.mw_listeners:
                    can_keep_scrolling = w.on_mousewheel(event)
                    if can_keep_scrolling:
                        # scroll_performed = True
                        break
        # if scroll_performed:
        #    print("scroll performed")

        # For now just stop event propagation.
        return "break"

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
        top = master.winfo_toplevel()
        if top not in cls.masters:
            cls.masters.append(top)
            # Bind to Enter event to prepare widgets
            top.bind_all("<Enter>", cls.on_mousewheel_enter, add="+")

            # Bind Wheel events to a specific class name
            # so we cant "break" the event and stop propagation
            _os = platform.system()
            if _os in ("Linux", "OpenBSD", "FreeBSD"):
                if tk.TkVersion >= 9:
                    top.bind_class(
                        cls.CLASS_NAME,
                        "<MouseWheel>",
                        cls.on_mousewheel,
                        add="+",
                    )
                else:
                    top.bind_class(
                        cls.CLASS_NAME, "<4>", cls.on_mousewheel, add="+"
                    )
                    top.bind_class(
                        cls.CLASS_NAME, "<5>", cls.on_mousewheel, add="+"
                    )
            else:
                # Windows and MacOS
                top.bind_class(
                    cls.CLASS_NAME,
                    "<MouseWheel>",
                    cls.on_mousewheel,
                    add="+",
                )

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
