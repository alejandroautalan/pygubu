#!/bin/sh

echo "============="
echo " $(python3 --version) (default python3)"

cd tests; python3 -m unittest; cd ..;


echo ""
echo "============="
echo " $(python2 --version) (default python2)"

cd tests; python2 -m unittest discover; cd ..;


echo ""
echo "============="
echo " Python 3.3.2 (custom build)"

cd tests; cpython3.3.2 -m unittest; cd ..;


echo ""
echo "============="
echo " Python 3.4.0 (custom build)"

cd tests; cpython3.4 -m unittest; cd ..;
