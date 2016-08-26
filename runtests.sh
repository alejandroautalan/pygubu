#!/bin/sh
python3bin=$(which python3)
echo " ============="
echo " Default Python 3: $python3bin "
echo " version: $($python3bin --version)"
echo " tk version :$($python3bin -c 'import tkinter; print(tkinter.TkVersion)')"

cd tests; $python3bin -m unittest; cd ..;


python2bin=$(which python)
echo " ============="
echo " Default Python 2: $python2bin"
echo " version: $($python2bin --version)"
echo " tk version :$($python2bin -c 'import Tkinter; print(Tkinter.TkVersion)')"

cd tests; $python2bin -m unittest discover; cd ..;


echo ""
echo "============="
echo " Python 3.3.2 (custom build)"
echo " tk 8.6 (debian package)"

cd tests; cpython3.3.2 -m unittest; cd ..;


echo ""
echo "============="
echo " Python 3.4.0 (custom build)"
echo " tk 8.6 (debian package)"

cd tests; cpython3.4 -m unittest; cd ..;
