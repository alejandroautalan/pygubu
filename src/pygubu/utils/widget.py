""" Widget utility functions."""


def crop_widget(widget, *, recursive=False):
    """Remove standard widget functionality."""

    # Remove standard bindings
    wclass = widget.winfo_class()
    bindtags = widget.bindtags()
    if wclass in bindtags:
        bindtags = list(bindtags)
        bindtags.remove(wclass)
        widget.bindtags(bindtags)
    # Don't take focus
    try:
        widget.configure(takefocus=False)
    except Exception:
        pass

    if recursive:
        for childw in widget.winfo_children():
            crop_widget(childw, recursive=recursive)
