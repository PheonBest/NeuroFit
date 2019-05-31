# -*- mode: python -*-

block_cipher = None

added_files = [
		 ( '../README.txt', '.' ),
		 ( '../LICENSE.md', '.' ),
		 ( '../GeometryAccuracy', 'GeometryAccuracy' ),
		 ( '../Missions', 'Missions' ),
		 ( '../Pendu', 'Pendu' ),
		 ( '../PhotoQuiz', 'PhotoQuiz' ),
		 ( '../input', 'input' ),
		 ( 'steganography', 'steganography' ),
         ( 'translate.csv', '.' ),
		 ( 'questsIcons', 'questsIcons' )
         ]
a = Analysis(['Hub.py'],
             pathex=['G:\\Documents\\GitHub\\NeuroFit\\Hub'],
             binaries=[],
             datas=added_files,
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
          name='Hub',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
