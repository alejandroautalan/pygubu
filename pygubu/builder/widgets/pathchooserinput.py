# encoding: utf8
from pygubu import BuilderObject, register_widget, register_property
from pygubu.widgets.pathchooserinput import PathChooserInput


class PathChooserInputBuilder(BuilderObject):
    class_ = PathChooserInput
    OPTIONS_CUSTOM = ('type', 'path', 'image', 'textvariable', 'state',
                      'initialdir', 'mustexist', 'title',)
    properties = OPTIONS_CUSTOM
    virtual_events = ('<<PathChooserPathChanged>>',)
    
    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == 'type':
            code_bag[pname] = "'{0}'".format(value)
        elif pname in ('initialdir', 'mustexist', 'title'):
            code_bag[pname] = "'{0}'".format(value)
        else:
            super(PathChooserInputBuilder, self)._code_set_property(
                targetid, pname, value, code_bag)


register_widget('pygubu.builder.widgets.pathchooserinput', PathChooserInputBuilder,
                'PathChooserInput', ('ttk', 'Pygubu Widgets'))

props = {
    'type': {
        'editor': 'choice',
        'params': {
            'values': (PathChooserInput.FILE, PathChooserInput.DIR), 'state': 'readonly'},
        'default': PathChooserInput.FILE,
        'help': 'Dialog type',
        },
    'path': {
        'editor': 'entry',
        'help': 'Initial path value.',
        },
    'image': {
        'editor': 'imageentry',
        'help': 'Image for the button.',
        },
    'textvariable': {
        'editor': 'tkvarentry',
        'help': 'Tk variable associated to the path property.',
        },
    'state': {
        'editor': 'choice',
        'pygubu.builder.widgets.pathchooserinput': {
            'params': {
                'values': ('', 'normal', 'disabled', 'readonly'),
                'state': 'readonly'},
            'help': 'Path entry state.',
            },
        },
    'mustexist': {
        'editor': 'dynamic',
        'params': {
            'mode': 'choice',
            'values': ('', 'false', 'true'), 'state': 'readonly'},
        'help': 'Dialog option. Determines if path must exist for directory dialog.'
        },
    'initialdir': {
        'editor': 'dynamic',
        'params': {'mode': 'entry'},
        'help': 'Dialog option. Sets initial directory.'
        },
    }

for p in props:
    register_property(p, props[p])

