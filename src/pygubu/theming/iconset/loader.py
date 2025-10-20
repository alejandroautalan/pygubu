import pathlib
import json
import importlib.resources as resources
import xml.etree.ElementTree as etree
import tkinter as tk
from contextlib import suppress
from pygubu.theming.iconset.iconset import IconSet
from pygubu.theming.iconset.photoreusable import PhotoImageReusable
from pygubu.theming.iconset.svgimage import HAS_SVG_SUPPORT, svg2photo
from pygubu.theming.photoresize import PhotoResizer


def change_icon_color(root: etree.ElementTree, fill):
    """Default color replace function for pygubu iconsets."""
    # Apply fill color override if provided
    pfill = "fill"
    pstroke = "stroke"
    color_none = "none"
    has_fill = root.attrib.get(pfill, None)
    has_stroke = root.attrib.get(pstroke, None)

    if not has_fill and not has_stroke:
        # Missing color information. FA Icon?
        root.attrib[pfill] = fill
    else:
        if has_fill and has_stroke:
            # Tabler icon ?
            fill_color = root.attrib.get(pfill, color_none)
            stroke_color = root.attrib.get(pstroke, color_none)
            if fill_color == color_none and stroke_color != color_none:
                root.attrib[pstroke] = fill
            if fill_color != color_none and stroke_color == color_none:
                root.attrib[pfill] = fill
        if has_fill and not has_stroke:
            # bootstrap icon ?
            root.attrib[pfill] = fill
        if has_fill == "currentColor":
            # some tabler filled icon?
            nodes = root.findall(".//*[@fill='currentColor']")
            for node in nodes:
                node.attrib[pfill] = fill


class IconSetLoader:
    """Loads images from iconset definition."""

    def __init__(self, data_module: str, data_filename: str):
        """Create a iconset loader.

        :param data_module: python module where images are stored.
        :param data_filename: filename containing json iconset definition.
        """
        self.master = None
        self.data_module = data_module
        self.data_filename = data_filename
        self.iconset = None
        self._theme = IconSet.THEME_LIGHT
        self.cache = {}

        with resources.open_binary(data_module, data_filename) as cf:
            self.iconset = IconSet(json.load(cf))

        self.has_bitmaps = self.iconset.with_png or self.iconset.with_gif
        self.bitmap_suffix = ".png" if tk.TkVersion >= 8.6 else ".gif"
        self.photo_resizer = None
        if self.has_bitmaps:
            self.photo_resizer = PhotoResizer()

    def _check_master(self):
        if self.master is None:
            raise RuntimeError("master is not configured")

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        theme_values = (IconSet.THEME_LIGHT, IconSet.THEME_DARK)
        if value not in theme_values:
            raise ValueError()
        self._theme = value
        if self.master is not None:
            self._reload_images()

    def _reload_images(self):
        self._check_master()
        for key, photo in self.cache.items():
            photo.tcl_keep()
            self._load_image(self.master, key)

    def get_image(self, master, image_uid):
        if image_uid in self.cache:
            return self.cache[image_uid]
        return self._load_image(master, image_uid)

    def _load_image(self, master, image_uid):
        if self.master is None and master is not None:
            self.master = master
        tkimage = None
        if HAS_SVG_SUPPORT:
            tkimage = self._load_svg_image(image_uid)
        elif self.has_bitmaps:
            tkimage = self._load_bitmap_image(image_uid)
        if tkimage is not None:
            self.cache[image_uid] = tkimage
        return tkimage

    def _load_svg_image(self, image_uid):
        tkimage = None
        if image_uid in self.iconset:
            fn, size, color_override, color = self.iconset.icon_props(
                image_uid, self._theme
            )
            replace_color_fun = change_icon_color if color_override else None
            with resources.open_binary(self.data_module, fn) as fileio:
                tkimage = svg2photo(
                    fileio,
                    fill=color,
                    modifier_fun=replace_color_fun,
                    scaletowidth=size,
                    master=self.master,
                    tcl_name=image_uid,
                )
        return tkimage

    def _load_bitmap_image(self, image_uid):
        img_final = None
        img_tmp = None
        fn, size, color_override, color = self.iconset.icon_props(
            image_uid, self._theme
        )
        bitmap_name = f"{self._theme}-{fn}"
        bitmap_name = pathlib.Path(bitmap_name).with_suffix(self.bitmap_suffix)
        with resources.path(self.data_module, bitmap_name) as fpath:
            img_tmp = tk.PhotoImage(master=self.master, file=str(fpath))
        img_final = self.photo_resizer.image_resize(
            img_tmp, size, size, PhotoImageReusable
        )

        return img_final

    def __call__(self, master, image_uid):
        return self.get_image(master, image_uid)
