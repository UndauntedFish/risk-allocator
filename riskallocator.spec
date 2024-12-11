# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['tradesorter.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
    a.binaries,
    a.datas,
    [],
    name='Risk Allocator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['bars.ico'],
    company_name='Evergreen Capital',
    product_name='Risk Allocator',
    description='This is the main program of the Risk Allocator, and contains all the logic necessary to generate a list of all the tickers and weigh them by sector exposure.',
    file_description='This is the main program of the Risk Allocator, and contains all the logic necessary to generate a list of all the tickers and weigh them by sector exposure.',
    copyright='© 2024 Evergreen Capital Everett, WA',
    version_resources=[r'./version.rc'],  # Ensure the relative path is correct
)
