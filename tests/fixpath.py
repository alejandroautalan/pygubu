import os
import sys
import pathlib
import importlib

test_dir = pathlib.Path(sys.argv[0]).parent.resolve()
pygubu_src = str(test_dir.parent / "src")

if pygubu_src not in sys.path:
    sys.path.insert(0, pygubu_src)
