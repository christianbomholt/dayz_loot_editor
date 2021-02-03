# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['G:\\LootEditor\\dayz_loot_editor\\\\app.py'],
             pathex=['C:\\Windows\\WinSxS\\x86_microsoft-windows-m..namespace-downlevel_31bf3856ad364e35_10.0.15063.0_none_7c5a1866018b960d', 'G:\\LootEditor\\dayz_loot_editor\\compiled'],
             binaries=[],
             datas=[],
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
          name='DayZ_LootEditor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='G:\\LootEditor\\dayz_loot_editor\\data\\LootEditor.ico')
