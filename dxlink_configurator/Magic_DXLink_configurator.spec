# -*- mode: python -*-
a = Analysis(['Magic_DXLink_configurator.py'],
             pathex=['C:\\Users\\jim.maciejewski\\Documents\\GitHub\\configurator\\dxlink_configurator'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Magic_DXLink_configurator.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon\\MDC_icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='Magic_DXLink_configurator')
