# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

python_files = [
  'main.py',
]

a = Analysis(python_files,
             pathex=[],
             binaries=[],
             datas=[('videogrep\\*.py', 'videogrep'), ('videogrep\\model', 'videogrep\\model'), ('.\\..\\Lib\\site-packages\\vosk', 'vosk')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='videogrep',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=['vcruntime140.dll', 'ucrtbase.dll'],
          runtime_tmpdir=None,
          console=True )
