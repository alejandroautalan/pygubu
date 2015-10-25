#!/usr/bin/python3
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
# For further info, check  http://pygubu.web.here

from __future__ import unicode_literals

import sys
import os
import argparse
import itertools
import xml.etree.ElementTree as ET

pygubu_basedir = os.path.abspath(os.path.dirname(
                    os.path.dirname(os.path.realpath(sys.argv[0]))))
if pygubu_basedir not in sys.path:
    sys.path.insert(0, pygubu_basedir)


from pygubu.builder import data_xmlnode_to_dict


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


class UI2Code(object):
    def __init__(self, uifile, object_id):
        self.uifile = uifile
        self.object_id = object_id
    
    def run(self):
        # Load ui definition from file
        self.tree = tree = ET.parse(self.uifile)
        self.root = tree.getroot()
        xpath = ".//object[@id='{0}']".format(self.object_id)
        node = self.tree.find(xpath)
        if node is not None:
            bobject = self._realize('', node)
    
    def _realize(self, master, node):
        data = data_xmlnode_to_dict(node)
        cname = data['class']
        uniqueid = data['id']
        
        print('# {0} widget'.format(uniqueid))
        stmt = "{0} = {1}({2})".format(uniqueid, cname, master)
        print(stmt)
        
        # properties
        prop_stmt = "{0}.configure({1})"
        arg_stmt = "{0}='{1}'"
        properties = data['properties']
        sorted_keys = sorted(properties.keys())
        for g in grouper(sorted_keys, 4):
            args_bag = []
            for p in g:
                if p is not None:
                    args_bag.append(arg_stmt.format(p, properties[p]))
            args = ', '.join(args_bag)
            print(prop_stmt.format(uniqueid, args))
        
        xpath = "./child"
        children = node.findall(xpath)
        for child in children:
            child_xml = child.find('./object')
            self._realize(uniqueid, child_xml)
        
        #layout:
        layout_stmt = "{0}.grid({1})"
        lrow_stmt = "{0}.rowconfigure({1}, {2})"
        lcol_stmt = "{0}.columnconfigure({1}, {2})"
        arg_stmt = "{0}='{1}'"
        layout = data['layout']
        if layout:
            args_bag = []
            for p, v in sorted(layout.items()):
                if p not in ('columns', 'rows', 'propagate'):
                    args_bag.append(arg_stmt.format(p, v))
            args = ', '.join(args_bag)
            print(layout_stmt.format(uniqueid, args))
            if 'propagate' in layout and layout['propagate'] == 'False': 
                print('{0}.propagate({1})'.format(uniqueid, layout['propagate']))
            # rows
            for idx, pd in layout['rows'].items():
                args_bag = []
                for p, v in sorted(pd.items()):
                    args_bag.append(arg_stmt.format(p, v))
                if args_bag:
                    args = ', '.join(args_bag)
                    print(lrow_stmt.format(uniqueid, idx, args))
            # cols
            for idx, pd in sorted(layout['columns'].items()):
                args_bag = []
                for p, v in sorted(pd.items()):
                    args_bag.append(arg_stmt.format(p, v))
                if args_bag:
                    args = ', '.join(args_bag)
                    print(lcol_stmt.format(uniqueid, idx, args))

def main():
    # Setup arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='.ui file')
    parser.add_argument('rootwidget', default='mainwindow', nargs='?',
                        help='Toplevel widget (default: mainwidow)')
    args = parser.parse_args()
    app = UI2Code(args.filename, args.rootwidget)
    app.run()


if __name__ == '__main__':
    main()
