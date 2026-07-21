# -*- mode: python ; coding: utf-8 -*-
# Build multiplateforme : Windows -> .exe (onefile) · macOS -> .app
import os
import sys
from PyInstaller.utils.hooks import collect_all

IS_MAC = sys.platform == "darwin"
IS_WIN = os.name == "nt"
SUF = ".exe" if IS_WIN else ""
FAST = os.environ.get("DEBUG_FAST") == "1"       # 1 -> sans ffmpeg (debug rapide)
CONSOLE = os.environ.get("DEBUG_CONSOLE") == "1"

# Icône selon la plateforme (optionnelle : le build ne casse pas si absente)
icon = None
if IS_WIN and os.path.exists("icon.ico"):
    icon = "icon.ico"
elif IS_MAC and os.path.exists("icon.icns"):
    icon = "icon.icns"

datas = [("index.html", "."), ("fonts", "fonts")]
if os.path.exists("icon.ico"):
    datas.append(("icon.ico", "."))

binaries = [("bundle_bin/yt-dlp" + SUF, ".")]
if not FAST:
    binaries += [("bundle_bin/ffmpeg" + SUF, ".")]

hiddenimports = ["clr"] if IS_WIN else []

# webview (+ backends) : pythonnet/clr sur Windows, pyobjc sur macOS
for pkg in ["webview", "clr_loader", "pythonnet", "proxy_tools", "bottle",
            "objc", "Foundation", "WebKit", "AppKit"]:
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass

a = Analysis(
    ["app.py"],
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

if IS_MAC:
    exe = EXE(
        pyz, a.scripts, a.binaries, a.datas, [],
        name="SWAYZ Downloader", debug=False, strip=False, upx=False,
        runtime_tmpdir=None, console=False, icon=icon,
    )
    app = BUNDLE(
        exe,
        name="SWAYZ Downloader.app",
        icon=icon,
        bundle_identifier="com.swayz.downloader",
        info_plist={
            "CFBundleName": "SWAYZ Downloader",
            "CFBundleDisplayName": "SWΛYZ Downloader",
            "CFBundleShortVersionString": "1.0.0",
            "NSHighResolutionCapable": True,
        },
    )
else:
    ONEFILE = os.environ.get("ONEFILE") == "1"
    if ONEFILE:
        exe = EXE(
            pyz, a.scripts, a.binaries, a.datas, [],
            name="SWAYZ Downloader", debug=False, bootloader_ignore_signals=False,
            strip=False, upx=False, runtime_tmpdir=None, console=CONSOLE,
            disable_windowed_traceback=False, icon=icon,
        )
    else:
        exe = EXE(
            pyz, a.scripts, [], exclude_binaries=True,
            name="SWAYZ Downloader", debug=False, bootloader_ignore_signals=False,
            strip=False, upx=False, console=CONSOLE,
            disable_windowed_traceback=False, icon=icon,
        )
        coll = COLLECT(
            exe, a.binaries, a.datas, strip=False, upx=False, upx_exclude=[],
            name="SWAYZ Downloader",
        )
