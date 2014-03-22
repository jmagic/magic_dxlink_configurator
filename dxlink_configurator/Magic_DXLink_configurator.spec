# -*- mode: python -*-
a = Analysis(['Magic_DXLink_configurator.py'],
             pathex=['C:\\Users\\jim.maciejewski\\Dropbox\\python_projects\\release\\dxlink_configurator\\dxlink_configurator'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Magic_DXLink_configurator.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon\\MDC_icon.ico')
