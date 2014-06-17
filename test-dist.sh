rm dist/* -rf
python setup.py sdist
cd dist/; tar xvzf pygubu-*.tar.gz ; cd pygubu-*; cpython3.4 setup.py install; cd ..; cd ..;
cpython3.4 ~/apps/cpython-3.4.0/bin/pygubu-designer
