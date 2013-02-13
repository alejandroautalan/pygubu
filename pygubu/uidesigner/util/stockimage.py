#
# Copyright 2012-2013 Alejandro Autalán
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  http://pygubu.web.here

__all__ = ['StockImage']

import os
import logging
import tkinter

stock_data = {}

logger = logging.getLogger('stockimage')


#class StockImage(Object):
class StockImage:
    """Maintain references to image name and file.
When image is used, the class maintains it on memory for tkinter"""
    _stock = stock_data
    _cached = {}


    @classmethod
    def register(cls, key, filename):
        if key in cls._stock:
            logger.info('Warning, replacing resource ' + str(key))
        cls._stock[key] = {'type': 'custom', 'filename': filename}
        logger.info('%s registered as %s' % (filename, key))


    @classmethod
    def register_from_dir(cls, dir_path):
        for filename in os.listdir(dir_path):
            filekey = filename.lower()
            if filekey.endswith('.gif'):
                cls.register(filekey[:-4], os.path.join(dir_path, filename))


    @classmethod
    def get(cls, rkey):
        if rkey in cls._cached:
            logger.info('Resource %s is in cache.' % rkey)
            return cls._cached[rkey]
        if rkey in cls._stock:
            v = cls._stock[rkey]
            img = None
            if v['type'] == 'stock':
                img = tkinter.PhotoImage(format=v['format'],data=v['data'])
            else:
                img = tkinter.PhotoImage(file=v['filename'])
            cls._cached[rkey] = img
            logger.info('Loaded resource %s.' % rkey)
            return img
        else:
            raise Exception('StockImage: %s not registered.' % rkey)

