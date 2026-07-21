<h1 align="center">SW&Lambda;YZ&nbsp;Downloader</h1>

<p align="center">
  <b>Free &amp; open-source video downloader for YouTube, TikTok, Instagram &amp; more.</b><br>
  Paste a link, pick the quality, download in the highest quality — video&nbsp;+&nbsp;sound (MP4&nbsp;H.264), or audio (MP3&nbsp;/&nbsp;WAV). No ads. No tracking. 100% free.
</p>

<p align="center">
  <img alt="Windows" src="https://img.shields.io/badge/Windows-10%2F11-50C98A">
  <img alt="macOS" src="https://img.shields.io/badge/macOS-supported-50C98A">
  <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-50C98A">
  <img alt="Price" src="https://img.shields.io/badge/Price-Free-50C98A">
  <img alt="Open source" src="https://img.shields.io/badge/Open%20source-yes-50C98A">
</p>

<p align="center">
  <a href="https://github.com/swayz-editing/swayz-downloader/releases/latest/download/SWAYZ-Downloader-Windows.exe">
    <img alt="Download for Windows" src="https://img.shields.io/badge/⬇%20Download%20for%20Windows-.exe-2ea043?style=for-the-badge&logo=windows">
  </a>
  &nbsp;
  <a href="https://github.com/swayz-editing/swayz-downloader/releases/latest/download/SWAYZ-Downloader-macOS.zip">
    <img alt="Download for macOS" src="https://img.shields.io/badge/⬇%20Download%20for%20macOS-.zip-2ea043?style=for-the-badge&logo=apple">
  </a>
</p>

<p align="center"><sub>One click, no setup. Or see all versions on the <a href="https://github.com/swayz-editing/swayz-downloader/releases/latest">Releases</a> page.</sub></p>

---

## ✨ What it does

A tiny, beautiful desktop app to **download videos for free**. You just paste a link — it shows a live preview (thumbnail, title, duration), lets you choose the quality, and saves the file wherever you want.

- 🎬 **Video + Sound** in **MP4 (H.264)** — plays *everywhere* and imports into any video editor (Premiere, After Effects…) **without errors**
- 🎵 **Audio only** — **MP3** (compressed) or **WAV** (uncompressed, for editing / sound design)
- ⚙️ **Quality picker** — Best / 4K / 1440p / 1080p / 720p / 480p / 360p (only shows what actually exists)
- 🔎 **Interactive preview** — paste a link and instantly see the thumbnail, title & duration
- 🖱️ **Drag & drop** a link straight onto the window
- 🔊 A little sound when the download finishes
- 🌍 **12 languages** with automatic detection (see below)
- 🔄 **Self-updating engine** — one click keeps it working when sites change
- 🚫 **No ads, no bundled junk, no account, no tracking** — and **fully open source**

Works with **YouTube, TikTok, Instagram, Vimeo, Twitter/X, Facebook** and hundreds of other sites (powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)).

---

## ⬇️ Download &amp; install

Grab the latest build from the **[Releases](../../releases)** page — nothing to install, everything is bundled inside.

### 🪟 Windows 10 / 11
1. Download **`SWAYZ Downloader.exe`** and double-click it.
2. On the first launch, Windows SmartScreen may warn you (it does that for any app that isn't code-signed). Click **“More info” → “Run anyway.”**

### 🍎 macOS
1. Download **`SWAYZ-Downloader-macOS.zip`**, unzip it, and move **SWAYZ Downloader.app** to Applications.
2. The app isn't signed with a paid Apple certificate, so the first time: **right-click the app → Open → Open**. You only do this once.

> Your friends need **zero** setup — the download engine and video toolkit are inside the app.
> Both builds are produced automatically by GitHub Actions (see [`.github/workflows/release.yml`](.github/workflows/release.yml)) — no Mac required to ship the Mac version.

---

## 🕹️ How to use

1. **Paste** a link (button, `Ctrl+V`, or drag it onto the window).
2. The app **analyzes** it and shows the thumbnail, title & duration.
3. Pick **Video + Sound** or **Audio**, then the **quality**.
4. Choose the **destination folder**.
5. Hit **Download**. Use **Open folder** to grab / share the file.

The output is always a clean **MP4 (H.264)** file that opens anywhere and imports into any editor without errors.

---

## 🔄 Keeping it up to date

Click **“⟳ Check for updates”** at the bottom of the app. It does two things:
- **Engine update** — video sites change often; if a link ever stops working, this fetches the latest download engine from GitHub and fixes itself, no re-install needed.
- **App update** — when a new version of SWΛYZ Downloader ships (new features), it points you straight to the download. *(Enabled once the project's GitHub repo is set in `APP_REPO` inside `app.py`.)*

---

## 🌍 Languages

Auto-detects your system language, with a picker in the top-left. Fully translated in:

**English · Français · العربية (RTL) · Español · Português · Deutsch · Italiano · Türkçe · Русский · Bahasa Indonesia · 中文 · हिन्दी**

Any other language falls back to English, so the app never breaks.

---

## 🛠️ Build from source

Requirements: **Python 3.10+** on Windows.

```bash
# 1. Dependencies
pip install pywebview pyinstaller

# 2. Provide the two engine binaries in a bundle_bin/ folder:
#    - bundle_bin/yt-dlp.exe   (https://github.com/yt-dlp/yt-dlp/releases/latest)
#    - bundle_bin/ffmpeg.exe   (https://ffmpeg.org/download.html — a Windows build)

# 3. Run it live (no build needed)
python app.py

# 4. Or build the standalone .exe
set ONEFILE=1 && pyinstaller --noconfirm build.spec
#   -> dist/SWAYZ Downloader.exe
```

### Project layout

| File | Role |
|---|---|
| `app.py` | Backend (pywebview): download, analyze, re-encode, updates |
| `index.html` | The whole UI + design + i18n (SWΛYZ art direction) |
| `fonts/` | Embedded fonts (Space Grotesk, Instrument Sans/Serif) |
| `icon.ico` / `make_icon.py` | App icon (+ generator) |
| `build.spec` | PyInstaller build recipe |

---

## ⚖️ Fair use

Please only download content **you own or have the right to use**, and respect each platform's Terms of Service. This tool is provided for personal and lawful use.

## 📄 License &amp; credits

- **SWΛYZ Downloader** source code — **MIT** (see [LICENSE](LICENSE)), free to use, modify and share.
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — Unlicense (the download engine).
- **[FFmpeg](https://ffmpeg.org)** — GPL/LGPL (video/audio processing). The packaged `.exe` includes a GPL build, so that binary is covered by the GPL.

---

<p align="center">Made with 💚 by <b>SW&Lambda;YZ</b> — free forever.</p>

<!--
Keywords (for search): free youtube downloader, download youtube videos free, tiktok video downloader,
instagram video downloader, open source video downloader, no ads video downloader, mp4 mp3 downloader,
windows video downloader, yt-dlp gui, 4k video downloader free, download video with sound.
-->
