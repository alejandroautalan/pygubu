# encoding: utf8
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

from __future__ import unicode_literals

__all__ = ['StockImage', 'StockImageException']

import os
import logging
try:
    import tkinter as tk
except:
    import Tkinter as tk


logger = logging.getLogger(__name__)
    

class StockImageException(Exception):
    pass


TK_IMAGE_FORMATS = ('.gif', '.pgm', '.ppm')

if tk.TkVersion >= 8.6:
    TK_IMAGE_FORMATS += ('.png',)


STOCK_DATA = {}


class StockImage(object):
    """Maintain references to image name and file.
When image is used, the class maintains it on memory for tkinter"""
    _stock = STOCK_DATA
    _cached = {}
    _formats = TK_IMAGE_FORMATS

    @classmethod
    def clear_cache(cls):
        """Call this before closing tk root"""
        #Prevent tkinter errors on python 2 ??
        for key in cls._cached:
            cls._cached[key] = None
        cls._cached = {}

    @classmethod
    def register(cls, key, filename):
        """Register a image file using key"""

        if key in cls._stock:
            logger.info('Warning, replacing resource ' + str(key))
        cls._stock[key] = {'type': 'custom', 'filename': filename}
        logger.info('%s registered as %s' % (filename, key))

    @classmethod
    def register_from_data(cls, key, format, data):
        """Register a image data using key"""

        if key in cls._stock:
            logger.info('Warning, replacing resource ' + str(key))
        cls._stock[key] = {'type': 'data', 'data': data, 'format': format }
        logger.info('%s registered as %s' % ('data', key))

    @classmethod
    def register_created(cls, key, image):
        """Register an already created image using key"""

        if key in cls._stock:
            logger.info('Warning, replacing resource ' + str(key))
        cls._stock[key] = {'type': 'created', 'image': image}
        logger.info('%s registered as %s' % ('data', key))

    @classmethod
    def is_registered(cls, key):
        return key in cls._stock

    @classmethod
    def register_from_dir(cls, dir_path, prefix=''):
        """List files from dir_path and register images with
            filename as key (without extension)
        Additionaly a prefix for the key can be provided,
        so the resulting key will be prefix + filename
        """

        for filename in os.listdir(dir_path):
            name, file_ext = os.path.splitext(filename)
            if file_ext in cls._formats:
                fkey = '{0}{1}'.format(prefix, name)
                cls.register(fkey, os.path.join(dir_path, filename))

    @classmethod
    def _load_image(cls, rkey):
        """Load image from file or return the cached instance."""

        v = cls._stock[rkey]
        img = None
        itype = v['type']
        if itype in ('stock', 'data'):
            img = tk.PhotoImage(format=v['format'], data=v['data'])
        elif itype == 'created':
            img = v['image']
        else:
            img = tk.PhotoImage(file=v['filename'])
        cls._cached[rkey] = img
        logger.info('Loaded resource %s.' % rkey)
        return img

    @classmethod
    def get(cls, rkey):
        """Get image previously registered with key rkey.
        If key not exist, raise StockImageException
        """

        if rkey in cls._cached:
            logger.info('Resource %s is in cache.' % rkey)
            return cls._cached[rkey]
        if rkey in cls._stock:
            img = cls._load_image(rkey)
            return img
        else:
            raise StockImageException('StockImage: %s not registered.' % rkey)
