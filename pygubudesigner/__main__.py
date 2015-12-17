import platform
import sys
import pygubu
from pygubudesigner import main

if __name__ == '__main__':
    # first of all, show the versions
    print("python version: {0} on {1}".format(platform.python_version(), sys.platform))
    print("pygubu version: {0}".format(pygubu.__version__))
    main.start_pygubu()
