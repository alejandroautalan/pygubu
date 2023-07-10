class StockImageException(Exception):
    pass


class ImageNotFoundError(StockImageException):
    pass


class ImageFormatNotSupportedError(StockImageException):
    pass
