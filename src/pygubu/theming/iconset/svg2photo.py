import os
import importlib.util
import tkinter as tk
from pygubu.theming.iconset.photoreusable import (
    PhotoImageReusable,
    ReusableImageMixin,
)
from pygubu.theming.iconset.svgedit import svgload


USE_TK9SVG = False
USE_TKSVG = False
USE_CAIROSVG = False

# Available svg backends: AUTO, TK9, TKSVG, CAIROSVG
USER_SVG_BACKEND = os.getenv("ICONSET_SVG_BACKEND", "AUTO")

if USER_SVG_BACKEND == "AUTO":
    if tk.TkVersion >= 9:
        USE_TK9SVG = True

    if not USE_TK9SVG:
        # try tksvg
        spec = importlib.util.find_spec("tksvg")
        if spec is not None:
            USE_TKSVG = True

    if not USE_TK9SVG and not USE_TKSVG:
        # try cairo svg
        spec = importlib.util.find_spec("cairosvg")
        if spec is not None:
            USE_CAIROSVG = True
elif USER_SVG_BACKEND == "TK9":
    USE_TK9SVG = True
elif USER_SVG_BACKEND == "TKSVG":
    USE_TKSVG = True
elif USER_SVG_BACKEND == "CAIROSVG":
    USE_CAIROSVG = True


if USE_TK9SVG:
    # Nothing to do here
    pass

if USE_TKSVG:
    import tksvg

    class SvgImageReusable(ReusableImageMixin, tksvg.SvgImage):
        """PhotoImage class to keep image names in tcl."""

        ...


if USE_CAIROSVG:
    import cairosvg


def svg2photo(
    source,
    *,
    color_override=False,
    fill=None,
    scaletowidth=None,
    scaletoheight=None,
    scale=None,
    master=None,
    tcl_name=None,
) -> tk.PhotoImage:
    """SVG to PhotoImage.
    Only one of scale, scaletowidth, scaletoheight
    is applied"""
    img_svg = svgload(source, color_override=color_override, fill=fill)
    img_data = img_svg.encode()

    tk_image = None
    if USE_TK9SVG:
        tk_image = tk9_svg2photo(
            img_data, scaletowidth, scaletoheight, scale, master, tcl_name
        )
    elif USE_TKSVG:
        tk_image = tksvg_svg2photo(
            img_data, scaletowidth, scaletoheight, scale, master, tcl_name
        )
    elif USE_CAIROSVG:
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
