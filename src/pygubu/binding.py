__all__ = ["remove_binding", "ApplicationLevelBindManager"]

import logging
import platform
import tkinter as tk

from pygubu.utils.widget import iter_to_toplevel


logger = logging.getLogger(__name__)


def bindings(widget, seq):
    return [x for x in widget.bind(seq).splitlines() if x.strip()]


def _funcid(binding):
    return binding.split()[1][3:]


def remove_binding(widget, seq, index=None, funcid=None):
    b = bindings(widget, seq)

    if index is not None:
        try:
            binding = b[index]
            widget.unbind(seq, _funcid(binding))
            b.remove(binding)
        except IndexError:
            logger.info("Binding #%d not defined.", index)
            return

    elif funcid:
        binding = None
        for x in b:
            if _funcid(x) == funcid:
                binding = x
                b.remove(binding)
                widget.unbind(seq, funcid)
                break
        if not binding:
            logger.info('Binding "%s" not defined.', funcid)
            return
    else:
        raise ValueError("No index or function id defined.")

    for x in b:
        widget.bind(seq, "+" + x, 1)


class AppBindManagerBase(object):
    # Acces to tk instance
    master: tk.Widget = None
    # Mouse wheel support
    mw_listeners = []  # Mousewheel listeners
    mw_initialized = False

    @classmethod
    def on_mousewheel(cls, event):
        widget_below = event.widget
        if not isinstance(widget_below, tk.Widget):
            try:
                widget_below = cls.master.winfo_containing(
                    event.x_root, event.y_root
                )
            except KeyError:
                widget_below = None
        if widget_below:
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
