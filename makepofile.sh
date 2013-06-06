#!/bin/sh

xgettext -L glade --output=po/pygubu.pot $(find ./pygubu/uidesigner/ui -name "*.ui")
xgettext --join-existing --language=Python --keyword=_ --output=po/pygubu.pot --from-code=UTF-8 `find ./pygubu/uidesigner -name "*.py"`
