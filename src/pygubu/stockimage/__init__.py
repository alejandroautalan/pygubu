from .registry import StockRegistry
from .loader import StockImageCache
from .exceptions import StockImageException
from .config import TK_BITMAP_FORMATS, TK_IMAGE_FORMATS, TK_PHOTO_FORMATS

DefaultRegistry = StockRegistry()

StockImage = StockImageCache(None, DefaultRegistry)
