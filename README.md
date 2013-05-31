Welcome to pygubu a GUI designer for tkinter
============================================

Pygubu is a RAD tool to enable quick & easy development of user interfaces
for the python tkinter.

The user interfaces designed are saved as XML, and by using the pygubu builder
these can be loaded by applications dynamically as needed.
Pygubu is inspired by Glade.

Installation
============

Pygubu requires python >= 2.7 (I tested only in python 2.7.3 and 3.2.3 with tk8.5)

Download and extract the tarball. Open a console in the extraction path
 and execute:

```
python setup.py install
```


Usage
=====

Create an UI definition using pygubu and save it to a file. Then, create
your aplication script as shown below:

```python
#test.py
import tkinter as tk
import pygubu

class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pugubu.Builder()

        #2: Load an ui file
        builder.add_from_file('test.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', master)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
```

See the examples directory or watch this hello world example on video http://youtu.be/wuzV9P8geDg


History
=======

Changes for version 0.7

  * Added python 2.7 support
  * Added initial TkApplication class
  * Fixed some bugs.
    
First public version 0.6
