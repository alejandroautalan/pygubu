import logging
from .exceptions import ImageFormatNotSupportedError, StockImageException
from .registry import StockRegistry, StockItem
from .config import _img_notsupported


logger = logging.getLogger(__name__)


class StockImageCache:
    IMAGE_NOT_SUPPORTED = "img_not_supported"

    def __init__(self, tkroot, registry: StockRegistry):
        self.tkroot = tkroot
        self.registry: StockRegistry = registry
        self._cached = {}
        if not registry.is_registered(self.IMAGE_NOT_SUPPORTED):
            self.register_from_data(
                self.IMAGE_NOT_SUPPORTED, "gif", _img_notsupported
            )

    def clear_cache(self):
        """Call this before closing tk root"""
        # Prevent tkinter errors on python 2 ??
        for key in self._cached:
            self._cached[key] = None
        self._cached = {}

    def register(self, image_id, filename):
        """Register a image file using image_id"""
        self.registry.register(image_id, filename)

    def register_from_package(self, image_id, fpath):
        self.registry.register_from_package(image_id, fpath)

    def register_from_data(self, image_id, format, data):
        """Register a image data using image_id"""
        self.registry.register_from_data(image_id, format, data)

    def register_created(self, image_id, image):
        """Register an already created image using image_id"""

        if image_id in self._cached:
            logger.warning("Warning, replacing resource {0}", image_id)
        self._cached[image_id] = image
        logger.info("data registered as %s", image_id)

    def is_registered(self, image_id):
        return image_id in self._cached or self.registry.is_registered(image_id)

    def register_all_from_dir(
        self, dir_path, prefix=None, ext=None, recurse=False
    ):
        self.registry.register_all_from_dir(dir_path, prefix, ext, recurse)

    def register_all_from_pkg(self, pkg, prefix=None, ext=None, recurse=False):
        self.registry.register_all_from_pkg(pkg, prefix, ext, recurse)

    def get(self, image_id, custom_loader=None):
        """Get image previously registered with key image_id.
        If key not exist, raise StockImageException
        """

        if image_id in self._cached:
            logger.info("Resource %s is in cache.", image_id)
            return self._cached[image_id]
        if self.registry.is_registered(image_id):
            img = self._load_image(image_id, custom_loader)
            return img
        else:
            raise StockImageException(f"StockImage: {image_id} not registered.")

    def _load_image(self, image_id, custom_loader=None):
        """Load image from file or return the cached instance."""

        stock_item: StockItem = self.registry.get_item(image_id)
        img = None
        try:
            img = stock_item.create_image(
                tk_master=self.tkroot, custom_loader=custom_loader
            )
        except ImageFormatNotSupportedError:
            msg = "Error loading image %s, try installing Pillow module."
            logger.error(msg, image_id)
            img = self.get(self.IMAGE_NOT_SUPPORTED)

        self._cached[image_id] = img
        logger.info("Loaded resource data for %s.", image_id)
        return img

    def as_iconbitmap(self, image_id):
        """Get image path for use in iconbitmap property"""
        return self.registry.as_iconbitmap(image_id)

    def add_resource_path(self, path):
        self.registry.add_resource_path(path)

    def add_resource_package(self, package):
        self.registry.add_resource_package(package)

    def find_and_register(self, image_id):
        self.registry.find_and_register(image_id)
