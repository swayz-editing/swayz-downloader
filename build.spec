# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

# DEBUG_FAST=1 -> ne pas embarquer ffmpeg (builds rapides pour debug)
FAST = os.environ.get("DEBUG_FAST") == "1"

datas = [('index.html', '.'), ('icon.ico', '.'), ('fonts', 'fonts')]
binaries = [('bundle_bin/yt-dlp.exe', '.')]
if not FAST:
    binaries += [('bundle_bin/ffmpeg.exe', '.')]
hiddenimports = ['clr']

for pkg in ['webview', 'clr_loader', 'pythonnet', 'proxy_tools', 'bottle']:
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

CONSOLE = os.environ.get("DEBUG_CONSOLE") == "1"
ONEFILE = os.environ.get("ONEFILE") == "1"

if ONEFILE:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name='SWAYZ Downloader',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        runtime_tmpdir=None,
        console=CONSOLE,
        disable_windowed_traceback=False,
        icon='icon.ico',
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='SWAYZ Downloader',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        console=CONSOLE,
        disable_windowed_traceback=False,
        icon='icon.ico',
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=False,
        upx_exclude=[],
        name='SWAYZ Downloader',
    )
