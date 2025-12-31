import pathlib
import json
import importlib.resources as resources
import xml.etree.ElementTree as etree
import tkinter as tk
from contextlib import suppress
from pygubu.theming.iconset.iconset import IconSet, IconItem, ThemeType
from pygubu.theming.iconset.photoreusable import PhotoImageReusable
from pygubu.theming.iconset.svgimage import HAS_SVG_SUPPORT, svg2photo
from pygubu.theming.photoresize import PhotoResizer


def change_icon_color(root: etree.ElementTree, fill):
    """Default color replace function for pygubu iconsets."""
    # Apply fill color override if provided
    FILL = "fill"
    STROKE = "stroke"
    STYLE = "style"
    COLOR_NONE = "none"

    # check if uses color information
    # some tabler filled icon? or new FA icons?
    colored_nodes = set(
        [node for node in root.findall("*[@fill]")]
        + [node for node in root.findall("*[@stroke]")]
    )
    root_has_color = any(
        (
            root.attrib.get(FILL, None),
            root.attrib.get(STROKE, None),
            root.attrib.get(STYLE, None),
        )
    )
    if root_has_color:
        colored_nodes.add(root)

    for node in colored_nodes:
        fill_color = root.attrib.get(FILL, COLOR_NONE)
        stroke_color = root.attrib.get(STROKE, COLOR_NONE)
        if fill_color == COLOR_NONE and stroke_color != COLOR_NONE:
            root.attrib[STROKE] = fill
        if fill_color != COLOR_NONE and stroke_color == COLOR_NONE:
            root.attrib[FILL] = fill

    if not colored_nodes:
        # Missing color information ?
        root.attrib[FILL] = fill


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
        self._theme = ThemeType.LIGHT
        self.cache = {}

        with resources.open_binary(data_module, data_filename) as cf:
            self.iconset = IconSet.from_dict(json.load(cf))

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
    def theme(self, value: ThemeType):
        if value not in ThemeType:
            raise ValueError()
        prev_value = self._theme
        self._theme = value
        do_reload = value != prev_value and self.master is not None
        if do_reload:
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

    def reload_image(self, master, image_uid, image_options: dict = None):
        """Reload image posible with custom options."""
        cached_image = self.cache.get(image_uid, None)
        if cached_image:
            cached_image.tcl_keep()
        return self._load_image(master, image_uid, image_options)

    def _load_image(self, master, image_uid, image_options: dict = None):
        if self.master is None and master is not None:
            self.master = master
        tkimage = None
        if image_uid in self.iconset:
            item: IconItem = self.iconset.item_on_theme(image_uid, self._theme)
            color = (
                item.color_onlight
                if self._theme == ThemeType.LIGHT
                else item.color_ondark
            )
            options = dict(
                fill=color,
                color_keep=item.color_keep,
                scaletowidth=item.width,
                master=self.master,
                tcl_name=image_uid,
            )
            if image_options:
                options.update(image_options)
            if HAS_SVG_SUPPORT:
                tkimage = self._load_svg_image(item.fn, options)
            elif self.has_bitmaps:
                tkimage = self._load_bitmap_image(item.fn, options)
        if tkimage is not None:
            self.cache[image_uid] = tkimage
        return tkimage

    def _load_svg_image(self, image_fn, image_options: dict):
        tkimage = None
        color_keep = image_options.pop("color_keep", False)
        image_options["modifier_fun"] = (
            change_icon_color if not color_keep else None
        )
        with resources.open_binary(self.data_module, image_fn) as fileio:
            tkimage = svg2photo(fileio, **image_options)
        return tkimage

    def _load_bitmap_image(self, image_fn, image_options: dict):
        img_final = None
        img_tmp = None
        bitmap_name = f"{self._theme.name.lower()}-{image_fn}"
        bitmap_name = pathlib.Path(bitmap_name).with_suffix(self.bitmap_suffix)
        with resources.path(self.data_module, bitmap_name) as fpath:
            img_tmp = tk.PhotoImage(master=self.master, file=str(fpath))
        size = image_options["scaletowidth"]
        tcl_name = image_options["tcl_name"]
        img_final = self.photo_resizer.image_resize(
            img_tmp, size, size, PhotoImageReusable, tcl_name
        )

        return img_final

    def __call__(self, master, image_uid):
        return self.get_image(master, image_uid)
