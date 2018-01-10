# -*- mode: python -*-

block_cipher = None


a = Analysis(['spc2py.py'],
             pathex=['C:\\Users\\Darrion\\Google Drive\\learn_web\\python\\python36\\spc2py'],
             binaries=[],
             datas=[
             ('config.ini', '.'),
             ('data\\*.csv', 'data'),
             ],
             hiddenimports=[],
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
          name='spc2py',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='app_icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='spc2py')
