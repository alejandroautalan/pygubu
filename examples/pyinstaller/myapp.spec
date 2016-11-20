# -*- mode: python -*-

block_cipher = None

# specify pygubu modules
hidden_imports = [
    'pygubu.builder.tkstdwidgets',
    'pygubu.builder.ttkstdwidgets',
    'pygubu.builder.widgets.dialog',
    'pygubu.builder.widgets.editabletreeview',
    'pygubu.builder.widgets.scrollbarhelper',
    'pygubu.builder.widgets.scrolledframe',
    'pygubu.builder.widgets.tkscrollbarhelper',
    'pygubu.builder.widgets.tkscrolledframe',
    'pygubu.builder.widgets.pathchooserinput',
]

data_files = [
    ('myapp.ui', '.'),
    ('imgs/*.gif', 'imgs'),
]

a = Analysis(['myapp.py'],
             pathex=['C:\\src\\pyinstaller'],
             binaries=None,
             datas=data_files,
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='myapp',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='myapp')
