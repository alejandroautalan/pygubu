#!/bin/sh

echo "============="
echo " Python 3.4.0 (debian package)"
echo " tk 8.6 (debian package)"

cd tests; python3.4 -m unittest; cd ..;


echo ""
echo "============="
echo " Python 2.7 (debian package)"
echo " tk 8.5 (debian package)"

cd tests; python2.7 -m unittest discover; cd ..;


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
