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
import locale
import os
import sys
from pathlib import Path

# Change this variable to your app name!
#  The translation files will be under
#  @LOCALE_DIR@/@LANGUAGE@/LC_MESSAGES/@APP_NAME@.mo
#
APP_NAME = "pygubu"

# Not sure in a regular desktop:

APP_DIR = Path(__file__).parent
LOCALE_DIR = APP_DIR / "locale"
FIRST_LC_MESSAGES_DIR = LOCALE_DIR / "de" / "LC_MESSAGES"
first_mo_file_path = FIRST_LC_MESSAGES_DIR / "pygubu.mo"
first_po_file_path = FIRST_LC_MESSAGES_DIR / "pygubu.po"

if not (first_po_file_path).exists():
    os.makedirs(FIRST_LC_MESSAGES_DIR, exist_ok=True)
    with open(first_po_file_path, "w") as f:
        f.write("")

if not (first_mo_file_path).exists():
    print(
        "You should compile the .po files in the pygubudesigner/locale "
        + "directory first if you are a developer, otherwise give us feedback "
        + "here: https://github.com/alejandroautalan/pygubu-designer/issues"
    )
    sys.exit(0)


# Now we need to choose the language. We will provide a list, and gettext
# will use the first translation available in the list
#
#  In maemo it is in the LANG environment variable
#  (on desktop is usually LANGUAGES)
#
DEFAULT_LANGUAGES = os.environ.get("LANG", "").split(":")

# Try to get the languages from the default locale
languages = []
lc, encoding = locale.getdefaultlocale()
if lc:
    languages = [lc]

# Concat all languages (env + default locale),
#  and here we have the languages and location of the translations
#
languages = DEFAULT_LANGUAGES + languages + ["en_US"]
mo_location = LOCALE_DIR

# Lets tell those details to gettext
#  (nothing to change here for you)
gettext.install(True)
gettext.bindtextdomain(APP_NAME, mo_location)
gettext.textdomain(APP_NAME)
language = gettext.translation(
    APP_NAME, mo_location, languages=languages, fallback=True
)

_ = translator = language.gettext


# And now in your modules you can do:
#
# import i18n
# _ = i18n.translator
#
