import gettext

#
# Keep pygubu as a simple library. Translations will be done in pygubu-designer repo.

_real_translator = gettext.gettext


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


_ = T = translator
