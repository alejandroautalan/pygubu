import logging
import sys
import tkinter as tk
from pathlib import Path
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from typing import Any
from .exceptions import ImageFormatNotSupportedError, ImageNotFoundError
from .config import (
    TK_IMAGE_FORMATS,
    TK_BITMAP_FORMATS,
    BITMAP_TEMPLATE,
    TK_PHOTO_FORMATS,
)


if sys.version_info < (3, 9):
    import importlib_resources as resources
else:
    import importlib.resources as resources


logger = logging.getLogger(__name__)


def _iter_package_files(pkg: str):
    subpkg = []
    try:
        for r in resources.files(pkg).iterdir():
            if r.is_file():
                yield r
            if r.is_dir():
                subpkg.append(r.name)
    except NotADirectoryError:
        pass
    for s in subpkg:
        yield from _iter_package_files(f"{pkg}/{s}")


class PitType(Enum):
    PATH = 1
    PACKAGE = 2


@dataclass
class StockItem:
    def create_image(self, *, tk_master=None, custom_loader=None):
        ...


@dataclass
class ImgFromPath(StockItem):
    fpath: Any = None

    def create_image(self, *, tk_master=None, custom_loader=None):
        file_ext = self.fpath.suffix.lower()
        if custom_loader is not None:
            img = custom_loader(PitType.PATH, self.fpath, tk_master)
        elif file_ext in TK_PHOTO_FORMATS:
            img = tk.PhotoImage(file=self.fpath, master=tk_master)
        elif file_ext in TK_BITMAP_FORMATS:
            img = tk.BitmapImage(file=self.fpath, master=tk_master)
        else:
            img = self._create_with_pillow(self.fpath, tk_master)
        return img

    def _create_with_pillow(self, fpath, tk_master):
        try:
            from PIL import Image, ImageTk

            aux = Image.open(fpath)
            img = ImageTk.PhotoImage(aux, master=tk_master)
            return img
        except ModuleNotFoundError:
            msg = f"Error loading {self.fpath}, image format not supported."
            raise ImageFormatNotSupportedError(msg)


@dataclass
class ImgFromPackage(ImgFromPath):
    def create_image(self, *, tk_master=None, custom_loader=None):
        file_ext = Path(str(self.fpath)).suffix.lower()

        with resources.as_file(self.fpath) as file:
            if custom_loader is not None:
                img = custom_loader(PitType.PACKAGE, file, tk_master)
            elif file_ext in TK_PHOTO_FORMATS:
                img = tk.PhotoImage(file=file, master=tk_master)
            elif file_ext in TK_BITMAP_FORMATS:
                img = tk.BitmapImage(file=file, master=tk_master)
            else:
                img = self._create_with_pillow(file, tk_master)
        return img


@dataclass
class ImgFromData(StockItem):
    data: Any = None
    format: str = None

    def create_image(self, *, tk_master=None, custom_loader=None):
        return tk.PhotoImage(
            format=self.format, data=self.data, master=tk_master
        )


class StockRegistry:
    """Maintain image source definitions to load."""

    def __init__(self):
        self._stock = {}
        self._formats = TK_IMAGE_FORMATS
        self._resource_pit = {}

    def _register_stock_item(self, image_id, cache_item):
        if image_id in self._stock:
            logger.warning("Warning, replacing resource %s", image_id)
        self._stock[image_id] = cache_item

    def register(self, image_id, filename):
        """Register a image file using image_id"""
        fpath = Path(filename) if isinstance(filename, str) else filename
        self._register_stock_item(image_id, ImgFromPath(fpath))
        logger.info("%s registered as %s", filename, image_id)

    def register_from_package(self, image_id, fpath):
        self._register_stock_item(image_id, ImgFromPackage(fpath))
        logger.info("%s registered as %s", fpath, image_id)

    def register_from_data(self, image_id, format, data):
        """Register a image data using image_id"""

        if image_id in self._stock:
            logger.warning("Warning, replacing resource %s", image_id)
        self._stock[image_id] = ImgFromData(data, format)
        logger.info("%s registered as %s", "data", image_id)

    def is_registered(self, image_id):
        return image_id in self._stock

    def get_item(self, image_id):
        return self._stock[image_id]

    def register_all_from_dir(
        self, dir_path, prefix=None, ext=None, recurse=False
    ):
        """List files from dir_path and register images with
            filename as key (without extension)

        :param str dir_path: path to search for images.
        :param str prefix: Additionaly a prefix for the key can be provided,
            so the resulting key will be prefix + filename
        :param iterable ext: list of file extensions to load. Defaults to
            tk supported image extensions. Example ('.jpg', '.png')
        :param boolean recurse: search recursivelly.
        """
        prefix = "" if prefix is None else prefix
        if ext is None:
            ext = TK_IMAGE_FORMATS

        path_gen = Path(dir_path).iterdir()
        if recurse:
            path_gen = Path(dir_path).glob("**/*")

        for filename in path_gen:
            if filename.is_file():
                name = filename.stem
                file_ext = filename.suffix
                if file_ext in ext:
                    fkey = f"{prefix}{name}"
                    self.register(fkey, filename)

    def register_all_from_pkg(self, pkg, prefix=None, ext=None, recurse=False):
        """List files from package and register images with
            filename as key (without extension)

        :param str pkg: package to search for images.
        :param str prefix: Additionaly a prefix for the key can be provided,
            so the resulting key will be prefix + filename
        :param iterable ext: list of file extensions to load. Defaults to
            tk supported image extensions. Example ('.jpg', '.png')
        :param boolean recurse: search recursivelly.
        """
        prefix = "" if prefix is None else prefix
        if ext is None:
            ext = TK_IMAGE_FORMATS
        path_gen = resources.files(pkg).iterdir()
        if recurse:
            path_gen = _iter_package_files(pkg)
        for pkg_path in path_gen:
            if pkg_path.is_file():
                fpath = Path(str(pkg_path))
                name = fpath.stem
                file_ext = fpath.suffix
                if file_ext in ext:
                    image_id = f"{prefix}{name}"
                    self.register_from_package(image_id, pkg_path)

    def add_resource_path(self, path):
        if path not in self._resource_pit:
            self._resource_pit[path] = PitType.PATH

    def add_resource_package(self, package):
        if package not in self._resource_pit:
            self._resource_pit[package] = PitType.PACKAGE

    def find_and_register(self, image_id):
        """Find and register image from the resource pits."""
        image_path = None
        pattern = f"*{image_id}"
        for pit, pit_type in self._resource_pit.items():
            if pit_type == PitType.PATH:
                try:
                    image_path = self._find_in_path(pit, pattern)
                except TypeError:
                    pass
                if image_path:
                    self.register(image_id, image_path)
                    break
            else:
                try:
                    image_path = self._find_in_package(pit, pattern)
                except ModuleNotFoundError:
                    pass
                if image_path:
                    self.register_from_package(image_id, image_path)
                    break
        if image_path is None:
            msg = f"Error: image {image_id} not found in resource pits."
            raise ImageNotFoundError(msg)

    @staticmethod
    def _find_in_path(path_src, pattern):
        found = None
        for p in Path(path_src).glob("**/*"):
            if p.is_file() and p.match(pattern):
                found = p
                break
        return found

    @staticmethod
    def _find_in_package(pkg_src, pattern):
        found = None
        for r in _iter_package_files(pkg_src):
            p2 = Path(str(r))
            if r.is_file() and p2.match(pattern):
                found = r
                break
        return found

    def as_iconbitmap(self, image_id):
        """Get image path for use in iconbitmap property"""
        img = None
        if image_id in self._stock:
            cache_item = self._stock[image_id]
            if isinstance(cache_item, ImgFromPath):
                fpath = cache_item.fpath
                file_ext = fpath.suffix.lower()

                if file_ext in TK_BITMAP_FORMATS:
                    img = BITMAP_TEMPLATE.format(fpath)
        return img
