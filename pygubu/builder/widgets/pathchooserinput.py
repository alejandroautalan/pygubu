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

_builder_id = 'pygubu.builder.widgets.pathchooserinput'
register_widget(_builder_id, PathChooserInputBuilder,
                'PathChooserInput', ('ttk', 'Pygubu Widgets'))

props = {
    'type': {
        'editor': 'dynamic',
        _builder_id : {
            'params': {
                'mode': 'choice',
                'values': (PathChooserInput.FILE, PathChooserInput.DIR),
                'state': 'readonly'},
            'default': PathChooserInput.FILE,
            'help': 'Dialog type',
            }
        },
    'path': {
        'editor': 'dynamic',
        _builder_id : {
            'params': {
                'mode': 'entry'},
            'help': 'Initial path value.',
            }
        },
    'image': {
        'editor': 'dynamic',
        _builder_id : {
            'params': {
                'mode': 'imageentry'},
            'help': 'Image for the button.',
            }
        },
    'textvariable': {
        'editor': 'dynamic',
        _builder_id : {
            'params': {
                'mode': 'tkvarentry'},
            'help': 'Tk variable associated to the path property.',
            }
        },
    'state': {
        'editor': 'dynamic',
        _builder_id : {
            'params': {
                'mode': 'choice',
                'values': ('', 'normal', 'disabled', 'readonly'),
                'state': 'readonly'},
            'help': 'Path entry state.',
            },
        },
    'mustexist': {
        'editor': 'dynamic',
        _builder_id : {
            'params': {
                'mode': 'choice',
                'values': ('', 'false', 'true'),
                'state': 'readonly'},
            'help': 'Dialog option. Determines if path must exist for directory dialog.'
            }
        },
    'initialdir': {
        'editor': 'dynamic',
        _builder_id : {
            'params': {'mode': 'entry'},
            'help': 'Dialog option. Sets initial directory.'
            }
        },
    'title': {
        'editor': 'dynamic',
        _builder_id : {
            'params': {'mode': 'entry'},
            'help': 'Dialog option. Sets dialog title.'
            }
        },
}

for p in props:
    register_property(p, props[p])

