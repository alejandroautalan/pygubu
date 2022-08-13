# encoding: utf-8
import re

RE_FONT = re.compile(
    "(?P<family>\\{\\w+(\\w|\\s)*\\}|\\w+)\\s?(?P<size>-?\\d+)?\\s?(?P<modifiers>\\{\\w+(\\w|\\s)*\\}|\\w+)?"
)


def tkfontstr_to_dict(fontstr):
    """Parse a string with a tk font format like '{Helvetica} 12 {bold}'
    and return a dict with keys family, size and modifiers."""

    font_dict = {
        "family": None,
        "size": None,
        "modifiers": None,
    }
    s = RE_FONT.search(fontstr)
    if s:
        g = s.groupdict()
        font_dict["family"] = g["family"].replace("{", "").replace("}", "")
        font_dict["size"] = g["size"]
        modifiers = g["modifiers"]
        if modifiers is not None:
            modifiers = modifiers.replace("{", "").replace("}", "")
            font_dict["modifiers"] = modifiers
    else:
        font_dict["family"] = fontstr
    return font_dict


def tkfontstr_to_tuple(fontstr, default_size=12):
    """Convert string with a tk font format like '{Helvetica} 12 {bold}'
    to a python tuple ('Helvetica', 12, 'bold')."""

    fdict = tkfontstr_to_dict(fontstr)
    font_desc = [
        fdict["family"],
    ]
    # Add default size
    size = fdict["size"]
    size = size if size is not None else default_size
    font_desc.append(size)

    key = "modifiers"
    if fdict[key] is not None:
        font_desc.append(fdict[key])

    return tuple(font_desc)
