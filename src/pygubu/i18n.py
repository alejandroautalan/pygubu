"""
Keep pygubu as a simple library. Translations will be done in pygubu-designer repo.

Here _ is used to mark strings in plugins files as translatable.

Do not use this file in your application projects.
"""

import os


def _real_translator(msg):
    return msg


_ = _real_translator


class LazyTranslator:
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return _real_translator(self._message)


def setup_translator(translator):
    global _real_translator
    _real_translator = translator


def translator(message: str) -> str:
    return LazyTranslator(message)


if "PYGUBU_LAZY_TRANSLATOR" in os.environ:
    # Environment variable is set in pygubu-designer to activate string translations.
    _ = T = translator
