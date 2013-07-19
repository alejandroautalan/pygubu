#!/bin/sh

xgettext -L glade --output=po/pygubu.pot $(find ./pygubudesigner/ui -name "*.ui")
xgettext --join-existing --language=Python --keyword=_ --output=po/pygubu.pot --from-code=UTF-8 `find ./pygubudesigner -name "*.py"`
