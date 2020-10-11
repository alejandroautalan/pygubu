rm ../sharedfolder/*.whl
python3 setup.py bdist_wheel
cp dist/*.whl ../sharedfolder
cd ..
cd pygubu-designer
python3 setup.py bdist_wheel
cp dist/*.whl ../sharedfolder
cd ../sharedfolder
python3 -m http.server 8080
