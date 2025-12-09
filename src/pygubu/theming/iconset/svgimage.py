import os
import importlib.util
import xml.etree.ElementTree as etree
import tkinter as tk

from enum import Enum, auto
from typing import Callable
from pygubu.theming.iconset.photoreusable import (
    PhotoImageReusable,
    ReusableImageMixin,
)


class SVGBackend(Enum):
    AUTO = auto()
    NONE = auto()
    TK9 = auto()
    TKSVG = auto()
    CAIROSVG = auto()


SVG_NAMESPACE = "http://www.w3.org/2000/svg"
etree.register_namespace("", SVG_NAMESPACE)
ETreeModifierFun = Callable[[etree.ElementTree, str], None]


# Available svg backends: AUTO, TK9, TKSVG, CAIROSVG
SVG_BACKEND = SVGBackend.NONE
USER_SVG_BACKEND = SVGBackend.AUTO
_env_backend = str(os.getenv("ICONSET_SVG_BACKEND", "AUTO")).upper()
try:
    USER_SVG_BACKEND = getattr(SVGBackend, _env_backend)
except AttributeError as e:
    msg = f"Invalid value '{_env_backend}' for ICONSET_SVG_BACKEND."
    raise ValueError(msg) from e

AVAILABLE_BACKENDS = []


def _check_svg_backends():
    if tk.TkVersion >= 9:
        AVAILABLE_BACKENDS.append(SVGBackend.TK9)
    # try tksvg
    spec = importlib.util.find_spec("tksvg")
    if spec is not None:
        AVAILABLE_BACKENDS.append(SVGBackend.TKSVG)
    # try cairo svg
    spec = importlib.util.find_spec("cairosvg")
    if spec is not None:
        AVAILABLE_BACKENDS.append(SVGBackend.CAIROSVG)
    if not AVAILABLE_BACKENDS:
        AVAILABLE_BACKENDS.append(SVGBackend.NONE)


_check_svg_backends()

if USER_SVG_BACKEND == SVGBackend.AUTO:
    SVG_BACKEND = AVAILABLE_BACKENDS[0]
elif USER_SVG_BACKEND in AVAILABLE_BACKENDS:
    SVG_BACKEND = USER_SVG_BACKEND
else:
    raise RuntimeError(f"SVG backend '{USER_SVG_BACKEND.name}' not available.")

HAS_SVG_SUPPORT = SVG_BACKEND != SVGBackend.NONE

if SVG_BACKEND == SVGBackend.TK9:
    # Nothing to do here
    pass

if SVG_BACKEND == SVGBackend.TKSVG:
    import tksvg

    class SvgImageReusable(ReusableImageMixin, tksvg.SvgImage):
        """PhotoImage class to keep image names in tcl."""

        ...


if SVG_BACKEND == SVGBackend.CAIROSVG:
    import cairosvg


def svg2photo(
    source,
    *,
    fill=None,
    modifier_fun: ETreeModifierFun = None,
    scaletowidth=None,
    scaletoheight=None,
    scale=None,
    master=None,
    tcl_name=None,
) -> tk.PhotoImage:
    """SVG to PhotoImage.
    Only one of scale, scaletowidth, scaletoheight
    is applied"""
    tree: etree.Element = etree.parse(source)
    root = tree.getroot()
    if callable(modifier_fun):
        modifier_fun(root, fill)
    svgdata = etree.tostring(root, "unicode")

    return photo_from_svgdata(
        svgdata, scaletowidth, scaletoheight, scale, master, tcl_name
    )


def photo_from_svgdata(
    data: str,
    scaletowidth=None,
    scaletoheight=None,
    scale=None,
    master=None,
    tcl_name=None,
) -> tk.PhotoImage:
    img_data = data.encode()
    tk_image = None
    if SVG_BACKEND == SVGBackend.TK9:
        tk_image = tk9_svg2photo(
            img_data, scaletowidth, scaletoheight, scale, master, tcl_name
        )
    elif SVG_BACKEND == SVGBackend.TKSVG:
        tk_image = tksvg_svg2photo(
            img_data, scaletowidth, scaletoheight, scale, master, tcl_name
        )
    elif SVG_BACKEND == SVGBackend.CAIROSVG:
        tk_image = cairosvg_svg2photo(
            img_data, scaletowidth, scaletoheight, scale, master, tcl_name
        )
    else:
        msg = (
            "No SVG image support installed. "
            "Use tk version 9 or install one of: tksvg, cairosvg"
        )
        raise RuntimeError(msg)

    return tk_image


def tk9_svg2photo(
    img_data,
    scaletowidth=None,
    scaletoheight=None,
    scale=None,
    master=None,
    tcl_name=None,
) -> PhotoImageReusable:
    photo_format = ["svg"]
    if scale:
        photo_format.extend(("-scale", scale))
    else:
        if scaletowidth:
            photo_format.extend(("-scaletowidth", scaletowidth))
        if scaletoheight:
            photo_format.extend(("-scaletoheight", scaletoheight))
    params = dict(
        data=img_data, format=photo_format, name=tcl_name, master=master
    )
    return PhotoImageReusable(**params)


def tksvg_svg2photo(
    img_data,
    scaletowidth=None,
    scaletoheight=None,
    scale=None,
    master=None,
    tcl_name=None,
) -> tk.PhotoImage:
    params = dict(data=img_data, name=tcl_name, master=master)
    if scale:
        params["scale"] = scale
    else:
        if scaletowidth:
            params["scaletowidth"] = scaletowidth
        if scaletoheight:
            params["scaletoheight"] = scaletoheight
    return SvgImageReusable(**params)


def cairosvg_svg2photo(
    img_data,
    scaletowidth=None,
    scaletoheight=None,
    scale=None,
    master=None,
    tcl_name=None,
) -> PhotoImageReusable:
    cairo_params = {}
    if scale:
        cairo_params["scale"] = scale
    elif scaletowidth:
        cairo_params["output_width"] = scaletowidth
    elif scaletoheight:
        cairo_params["output_height"] = scaletoheight
    png_data = cairosvg.svg2png(img_data, **cairo_params)
    kw = dict(data=png_data, format="png")
    return PhotoImageReusable(name=tcl_name, master=master, **kw)
