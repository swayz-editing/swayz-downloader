<h1 align="center">SW&Lambda;YZ&nbsp;Downloader</h1>

<p align="center">
  <b>Free &amp; open-source video downloader for YouTube, TikTok, Instagram &amp; more.</b><br>
  Paste a link, pick the quality, download in the highest quality — video&nbsp;+&nbsp;sound (MP4&nbsp;H.264), or audio (MP3&nbsp;/&nbsp;WAV). No ads. No tracking. 100% free.
</p>

<p align="center">
  <img alt="Windows" src="https://img.shields.io/badge/Windows-10%2F11-50C98A">
  <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-50C98A">
  <img alt="Price" src="https://img.shields.io/badge/Price-Free-50C98A">
  <img alt="Open source" src="https://img.shields.io/badge/Open%20source-yes-50C98A">
</p>

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

## ⬇️ Download &amp; install (Windows)

1. Go to the **[Releases](../../releases)** page and download **`SWAYZ Downloader.exe`**.
2. Double-click it. Nothing to install — everything is included.
3. On the first launch, Windows SmartScreen may warn you (it does that for any app that isn't code-signed). Click **“More info” → “Run anyway.”**

> Requires Windows 10 or 11. The file is ~100&nbsp;MB because the download engine and the video toolkit are bundled inside — your friends need **zero** setup.

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

Video sites change often. If a link ever stops working, click **“⟳ Check for updates”** at the bottom of the app — it fetches the latest engine from GitHub and fixes itself. No re-install needed.

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
