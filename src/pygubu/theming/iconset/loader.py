import pathlib
import json
import importlib.resources as resources
from contextlib import suppress
from pygubu.theming.iconset.iconset import IconSet
from pygubu.theming.iconset.photoreusable import PhotoImageReusable
from pygubu.theming.iconset.svg2photo import svg2photo


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
        if image_uid in self.iconset:
            fn, size, color_override, color = self.iconset.icon_props(
                image_uid, self._theme
            )
            with resources.open_binary(self.data_module, fn) as fileio:
                tkimage = svg2photo(
                    fileio,
                    color_override=color_override,
                    fill=color,
                    scaletowidth=size,
                    master=master,
                    tcl_name=image_uid,
                )
                self.cache[image_uid] = tkimage
        return tkimage

    def __call__(self, master, image_uid):
        return self.get_image(master, image_uid)
