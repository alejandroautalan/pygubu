# encoding: utf-8
import logging
import tkinter as tk


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
