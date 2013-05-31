#!/bin/sh

echo "============="
echo "Python 3 tests"

cd tests; python3 -m unittest; cd ..;

echo ""
echo "============="
echo "Python 2.7 tests"

cd tests; python2.7 -m unittest discover; cd ..;


