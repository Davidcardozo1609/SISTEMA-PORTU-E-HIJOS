# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Archivo_ejecutar.py'],
    pathex=[],
    binaries=[],
    datas=[('logo.png', '.'), ('flecha.png', '.'), ('PANTALLA PRINCIPAL.png', '.'), ('imagen_mostrar_contra.jpeg', '.'), ('imagen_contra.jpeg', '.')],
    hiddenimports=['tkcalendar', 'PIL.ImageTk'],
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
    a.binaries,
    a.datas,
    [],
    name='MB_LENCERIA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['MB.ico'],
)
