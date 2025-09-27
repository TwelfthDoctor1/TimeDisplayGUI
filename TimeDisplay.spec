# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/twelfthdoctor1/GitHub/TimeDisplayGUI/TimeDisplay.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/twelfthdoctor1/GitHub/TimeDisplayGUI/Resources', 'Resources')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TimeDisplay',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/Users/twelfthdoctor1/GitHub/TimeDisplayGUI/Resources/TimeDisplayIcon_V2.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TimeDisplay',
)
app = BUNDLE(
    coll,
    name='TimeDisplay.app',
    icon='/Users/twelfthdoctor1/GitHub/TimeDisplayGUI/Resources/TimeDisplayIcon_V2.png',
    bundle_identifier=None,
)
