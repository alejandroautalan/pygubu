#!/bin/sh
python3bin=$(which python3)
echo " ============="
echo " Default Python 3: $python3bin "
echo " version: $($python3bin --version)"
echo " tk version :$($python3bin -c 'import tkinter; print(tkinter.TkVersion)')"

cd tests; $python3bin -m unittest; cd ..;

#echo ""
#echo "============="
#echo " Python 3.6.15 (custom build)"
#echo " tk 8.6 (debian package)"
#
#cd tests; cpython3.6 -m unittest; cd ..;
