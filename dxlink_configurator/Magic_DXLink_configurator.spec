# -*- mode: python -*-
a = Analysis(['Magic_DXLink_configurator.py'],
             pathex=['C:\\Users\\kylie\\Documents\\configurator\\dxlink_configurator'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
##### include mydir in distribution #######
def extra_datas(icon):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % icon, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'icon'))

    return extra_datas
###########################################
a.datas += extra_datas('icon')
a.datas += extra_datas('media')
a.datas += extra_datas('sounds')
a.datas += extra_datas('send_commands')
a.datas += extra_datas('docs')
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Magic_DXLink_configurator.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='icon\\MDC_icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='Magic_DXLink_configurator')
