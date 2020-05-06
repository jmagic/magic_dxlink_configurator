# -*- mode: python -*-

block_cipher = None

project_name = 'magic_dxlink_configurator'
project_version = 'v4.0.3'
project_icon = 'mdc.ico'
single_file = False

## Do not modify below this line.


a = Analysis([f'{project_name}.py'],
             pathex=[f'C:\\Users\\jimm\\Documents\\{project_name}'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

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
############################################
a.datas += extra_datas('icon')
a.datas += extra_datas('doc')


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=f'{project_name}.exe',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon=f'icon\\{project_icon}' )

if not single_file:
    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=None,
                   upx=True,
                   name=project_name)

#######################################
# Code-sign the generated executable
import subprocess
subprocess.call(["C:\\Program Files (x86)\\Windows Kits\\10\\bin\\x64\\signtool.exe",
                 "sign",
                 "/f", "C:\\Users\\jimm\\Nextcloud\\WindowsSigningCert\\MyKey.pfx",
                 "/t", "http://timestamp.comodoca.com/authenticode",
                 "/p", "9fQo2YmntgPPb8eQ",
                 f"C:\\Users\\jimm\\Documents\\{project_name}\\dist\\{project_name}.exe",
])
#"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe" sign /f "C:\Users\jimm\Nextcloud\WindowsSigningCert\MyKey.pfx" /t http://timestamp.comodoca.com/authenticode /p 9fQo2YmntgPPb8eQ $f
#######################################