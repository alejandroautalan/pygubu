import logging
import platform
import tkinter as tk

from pygubu.utils.widget import iter_to_toplevel


logger = logging.getLogger(__name__)


class AppBindManagerBase(object):
    # Acces to tk instance
    master: tk.Widget = None
    # Mouse wheel support
    mw_listeners = []  # Mousewheel listeners
    mw_initialized = False

    @classmethod
    def on_mousewheel(cls, event):
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
        if _os in ("Linux", "OpenBSD", "FreeBSD"):
            if tk.TkVersion >= 9:

                def on_mousewheel(event):
                    view_command(
                        "scroll",
                        (-1) * int((event.delta / 120) * factor),
                        "units",
                    )
                    scroll_rs = view_command()
                    if scroll_rs is None:
                        return False
                    can_keep_scrolling = scroll_rs[0] != 0.0
                    if event.delta < 0:
                        can_keep_scrolling = scroll_rs[1] != 1.0
                    return can_keep_scrolling

            else:

                def on_mousewheel(event):
                    can_keep_scrolling = True
                    if event.num == 4:
                        view_command("scroll", (-1) * factor, "units")
                        scroll_rs = view_command()
                        can_keep_scrolling = scroll_rs[0] != 0.0
                    elif event.num == 5:
                        view_command("scroll", factor, "units")
                        scroll_rs = view_command()
                        can_keep_scrolling = scroll_rs[1] != 1.0
                    return can_keep_scrolling

        elif _os == "Windows":

            def on_mousewheel(event):
                view_command(
                    "scroll", (-1) * int((event.delta / 120) * factor), "units"
                )
                scroll_rs = view_command()
                can_keep_scrolling = scroll_rs[0] != 0.0
                if event.delta < 0:
                    can_keep_scrolling = scroll_rs[1] != 1.0
                return can_keep_scrolling

        elif _os == "Darwin":

            def on_mousewheel(event):
                view_command("scroll", event.delta, "units")
                scroll_rs = view_command()
                can_keep_scrolling = scroll_rs[0] != 0.0
                if event.delta < 0:
                    can_keep_scrolling = scroll_rs[1] != 1.0
                return can_keep_scrolling

        else:
            # FIXME: unknown platform scroll method
            def on_mousewheel(event):
                pass

        return on_mousewheel


class ApplicationLevelBindManager(AppBindManagerBase):
    ...
