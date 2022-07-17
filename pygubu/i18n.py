#
# Copyright 2012-2022 Alejandro Autalán
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

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
