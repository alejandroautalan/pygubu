""" Widget utility functions."""


def crop_widget(widget, *, recursive=False):
    """Remove standard widget functionality."""
    wclass = widget.winfo_class()
    bindtags = widget.bindtags()
    if wclass in bindtags:
        bindtags = list(bindtags)
        bindtags.remove(wclass)
        widget.bindtags(bindtags)
    if recursive:
        for childw in widget.winfo_children():
            crop_widget(childw, recursive=recursive)
