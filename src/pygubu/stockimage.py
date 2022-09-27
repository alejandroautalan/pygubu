# encoding: utf-8

__all__ = ["StockImage", "StockImageException", "TK_IMAGE_FORMATS"]

import logging
import os
import sys
import tkinter as tk
from pathlib import Path
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from typing import Any


if sys.version_info < (3, 9):
    import importlib_resources as resources
else:
    import importlib.resources as resources


logger = logging.getLogger(__name__)


class StockImageException(Exception):
    pass


class ImageNotFoundError(StockImageException):
    pass


class ImageFormatNotSupportedError(StockImageException):
    pass


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


BITMAP_TEMPLATE = "@{0}"
TK_BITMAP_FORMATS = [".xbm"]
TK_PHOTO_FORMATS = [".gif", ".pgm", ".ppm"]


if os.name == "nt":
    TK_BITMAP_FORMATS.append(".ico")
    BITMAP_TEMPLATE = "{0}"

if tk.TkVersion >= 8.6:
    TK_PHOTO_FORMATS.append(".png")


TK_IMAGE_FORMATS = TK_PHOTO_FORMATS + TK_BITMAP_FORMATS


_img_notsupported = """\
R0lGODlhZAAyAIQAAAAAAAsLCxMTExkZGSYmJicnJ11dXYGBgZubm5ycnJ2dnbGxsbOzs8TExMXF
xdXV1dbW1uTk5PLy8v39/f7+/v///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEK
AB8ALAAAAABkADIAAAX+4CeOZGmeaKqubOu+cCzPMmDfeK7vfO//QJ5rQCwaj8ikcslsOpUswGBC
qVqv2Kx2y+16v9nJAKAaFCiVtHrNbrvf8Lh83qYUBigplc7v+/9yFGJkJVJogIiJinAUYyaGi5GS
iI2EJJBuDQ0UChFqmmkNCAqHnAijFKKnnmoRpwgNoagVrqexFaBpEaS0qxWms26VjwOHbaeNDJ4Q
BwgVEAsICQ8SEg8Jp6QIBr5qEAG2z9HTEt+nCxAVCAfpEQzFEQ6nDhGcBga8wo6FxW/IAwISTCAA
rtEDQQMgQChmRR2CKmwWUqmS8FdCiRQenEEQgMCEBAKKIaNwKk1JRvv+LvVz8+/BA4//Qo5RWEyB
GZIBiKTzJmUAqYqNFPZMgObUQJcicw4AZ9IZSksjMB17mLCcw2QQHgigScGdSHYQJKyBIOABhHpA
L5Zt1vRZua8K2TqMM4yfMTb/dl5Ne3YaBAfawIr1tpKTg6wJIixMhW5umsUnIzt9U1fl3TUKSBXQ
m9lOOs+/7ihIY1Pn2DOYbz5DDeFMZm+uR1d4PVs25ZRRV9ZBcxeisd8QfzVkc3n4LzW8ewtPEzz4
bagipE6aTl0f9A/Sq2unXjm3cuTImxtfc2X58vLMxztHL9x3Q/bIcUfX3brU5tA+SRfRy/zOTdqd
+cdaEbYtBJSAaBj+6JMdRLi2H3HyYUcfOJ4EFYFfgHXFQFmD6eKXQo79wwBiipX1FykNoAPNJgOM
eE0E1gigDFbprKPQArcwF6FU5tAT1GLP9APkGheaxYpkWL1IllkZItkiiRZ99mSNTp2k43U81iTQ
RUJ2eRl+RIVIVUis9SSbkwKEVEpaZJJU5WQWYUkfQw/MBOSdupGX0UZvGhQcRoc4idSaUh5U1Jvk
7TgnGjGGdQ0CjQV5WS2QtiMPAj5WRNhd8cyDlqOJRWlRM9pwgykrVxJjzC6ldPKLArC0kk8rr+RY
S4WuyjqpL5zg6uur2aTyCqqp2rXdsdwp+iWyzP7R3Xx7NCutHwiGXSeCatNmS9cdKugBxre7fSvu
uFcMwsIT6KKGnH/otuuuES4EIW+elchr77050ECDdM/q6++/M/AbIcAEF5yCwNYarLDC2P5i7sIQ
K+ztunhEbHHBUlV78cb/YsIgxyDr663GIZcMgw3wmqxyvPmu7HIeCb8sc1Qxz2zzzTjnrPPOPPcs
QwgAOw==
"""


class PitType(Enum):
    PATH = 1
    PACKAGE = 2


@dataclass
class CacheItem:
    def create_tkimage(self):
        ...


@dataclass
class ImgFromData(CacheItem):
    data: Any = None
    format: str = None

    def create_tkimage(self):
        tk.PhotoImage(format=self.format, data=self.data)


@dataclass
class ImgCreated(CacheItem):
    image: Any = None

    def create_tkimage(self):
        return self.image


@dataclass
class ImgFromPath(CacheItem):
    fpath: Any = None

    def _create_with_pillow(self, fpath):
        try:
            from PIL import Image, ImageTk

            aux = Image.open(fpath)
            img = ImageTk.PhotoImage(aux)
            return img
        except ModuleNotFoundError:
            msg = f"Error loading {self.fpath}, image format not supported."
            raise ImageFormatNotSupportedError(msg)

    def create_tkimage(self):
        file_ext = self.fpath.suffix.lower()
        if file_ext in TK_PHOTO_FORMATS:
            img = tk.PhotoImage(file=self.fpath)
        elif file_ext in TK_BITMAP_FORMATS:
            img = tk.BitmapImage(file=self.fpath)
        else:
            img = self._create_with_pillow(self.fpath)
        return img


@dataclass
class ImgFromPackage(ImgFromPath):
    def create_tkimage(self):
        file_ext = Path(str(self.fpath)).suffix.lower()

        with resources.as_file(self.fpath) as file:
            if file_ext in TK_PHOTO_FORMATS:
                img = tk.PhotoImage(file=file)
            elif file_ext in TK_BITMAP_FORMATS:
                img = tk.BitmapImage(file=file)
            else:
                img = self._create_with_pillow(file)
        return img


STOCK_DATA = {"img_not_supported": ImgFromData(_img_notsupported, "gif")}


class StockImage:
    """Maintain references to image name and file.
    When image is used, the class maintains it on memory for tkinter"""

    _stock = STOCK_DATA
    _cached = {}
    _formats = TK_IMAGE_FORMATS
    _resource_pit = {}

    @classmethod
    def clear_cache(cls):
        """Call this before closing tk root"""
        # Prevent tkinter errors on python 2 ??
        for key in cls._cached:
            cls._cached[key] = None
        cls._cached = {}

    @classmethod
    def _register_cache_item(cls, image_id, cache_item):
        if image_id in cls._stock:
            logger.warning("Warning, replacing resource %s", image_id)
        cls._stock[image_id] = cache_item

    @classmethod
    def register(cls, image_id, filename):
        """Register a image file using image_id"""
        fpath = Path(filename) if isinstance(filename, str) else filename
        cls._register_cache_item(image_id, ImgFromPath(fpath))
        logger.info("%s registered as %s", filename, image_id)

    @classmethod
    def register_from_package(cls, image_id, fpath):
        cls._register_cache_item(image_id, ImgFromPackage(fpath))
        logger.info("%s registered as %s", fpath, image_id)

    @classmethod
    def register_from_data(cls, image_id, format, data):
        """Register a image data using image_id"""

        if image_id in cls._stock:
            logger.warning("Warning, replacing resource %s", image_id)
        cls._stock[image_id] = ImgFromData(data, format)
        logger.info("%s registered as %s", "data", image_id)

    @classmethod
    def register_created(cls, image_id, image):
        """Register an already created image using image_id"""

        if image_id in cls._stock:
            logger.warning("Warning, replacing resource {0}", image_id)
        cls._stock[image_id] = ImgCreated(image)
        logger.info("data registered as %s", image_id)

    @classmethod
    def is_registered(cls, image_id):
        return image_id in cls._stock

    @classmethod
    def register_all_from_dir(
        cls, dir_path, prefix=None, ext=None, recurse=False
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
                    cls.register(fkey, filename)

    @classmethod
    def register_all_from_pkg(cls, pkg, prefix=None, ext=None, recurse=False):
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
                    cls.register_from_package(image_id, pkg_path)

    @classmethod
    def _load_image(cls, image_id):
        """Load image from file or return the cached instance."""

        cache_info = cls._stock[image_id]
        img = None
        try:
            img = cache_info.create_tkimage()
        except ImageFormatNotSupportedError:
            msg = "Error loading image %s, try installing Pillow module."
            logger.error(msg, image_id)
            img = cls.get("img_not_supported")

        cls._cached[image_id] = img
        logger.info("Loaded resource data for %s.", image_id)
        return img

    @classmethod
    def get(cls, image_id):
        """Get image previously registered with key image_id.
        If key not exist, raise StockImageException
        """

        if image_id in cls._cached:
            logger.info("Resource %s is in cache.", image_id)
            return cls._cached[image_id]
        if image_id in cls._stock:
            img = cls._load_image(image_id)
            return img
        else:
            raise StockImageException(f"StockImage: {image_id} not registered.")

    @classmethod
    def as_iconbitmap(cls, image_id):
        """Get image path for use in iconbitmap property"""
        img = None
        if image_id in cls._stock:
            data = cls._stock[image_id]
            if data["type"] not in ("stock", "data", "image"):
                fpath = data["filename"]
                file_ext = fpath.suffix.lower()

                if file_ext in TK_BITMAP_FORMATS:
                    img = BITMAP_TEMPLATE.format(fpath)
        return img

    @classmethod
    def add_resource_path(cls, path):
        if path not in cls._resource_pit:
            cls._resource_pit[path] = PitType.PATH

    @classmethod
    def add_resource_package(cls, package):
        if package not in cls._resource_pit:
            cls._resource_pit[package] = PitType.PACKAGE

    @classmethod
    def find_and_register(cls, image_id):
        """Find and register image from the resource pits."""
        image_path = None
        pattern = f"*{image_id}"
        for pit, pit_type in cls._resource_pit.items():
            if pit_type == PitType.PATH:
                try:
                    image_path = cls._find_in_path(pit, pattern)
                except TypeError:
                    pass
                if image_path:
                    cls.register(image_id, image_path)
                    break
            else:
                try:
                    image_path = cls._find_in_package(pit, pattern)
                except ModuleNotFoundError:
                    pass
                if image_path:
                    cls.register_from_package(image_id, image_path)
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
