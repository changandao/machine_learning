# -*- mode: python -*-

block_cipher = None


a = Analysis(['PyClassificationToolbox.py'],
             pathex=['/home/steidl/PyDevWorkspace/PyClassificationToolbox'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=['.'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('version.json', 'version.json', 'DATA'), ('GPLv3.html', 'GPLv3.html', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          Tree('./img', prefix='img'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='PyClassificationToolbox',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='PyClassificationToolbox.ico')
