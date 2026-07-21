# -*- coding: utf-8 -*-
"""
SWΛYZ — Téléchargeur vidéo / audio
Interface HTML/CSS dans une fenêtre native (pywebview) + yt-dlp / ffmpeg.
"""

import os
import io
import re
import sys
import json
import ctypes
import threading
import subprocess

import webview

APP_DIR = os.path.dirname(os.path.abspath(__file__))
FROZEN = getattr(sys, "frozen", False)


def resource_path(name):
    """Chemin d'une ressource embarquée (fonctionne en .py comme en .exe)."""
    base = getattr(sys, "_MEIPASS", APP_DIR)
    return os.path.join(base, name)


def data_dir():
    """Dossier durable pour la config (survit au .exe onefile)."""
    d = os.path.join(os.environ.get("APPDATA") or os.path.expanduser("~"), "SWAYZ")
    try:
        os.makedirs(d, exist_ok=True)
    except Exception:
        return APP_DIR
    return d


CONFIG_PATH = os.path.join(data_dir(), "config.json")
INDEX = resource_path("index.html")
ICON = resource_path("icon.ico")

APP_VERSION = "1.0.0"

# Binaires : embarqués dans le .exe, sinon depuis le PATH
YTDLP = resource_path("yt-dlp.exe") if FROZEN else "yt-dlp"
FFMPEG_DIR = getattr(sys, "_MEIPASS", None) if FROZEN else None
FFMPEG = os.path.join(FFMPEG_DIR, "ffmpeg.exe") if FFMPEG_DIR else "ffmpeg"

# yt-dlp mis à jour (téléchargé dans APPDATA) — a priorité sur celui embarqué,
# ce qui permet de mettre à jour le moteur sans reconstruire l'exe.
UPDATED_YTDLP = os.path.join(data_dir(), "yt-dlp.exe")


def ytdlp_path():
    try:
        if os.path.exists(UPDATED_YTDLP) and os.path.getsize(UPDATED_YTDLP) > 1_000_000:
            return UPDATED_YTDLP
    except Exception:
        pass
    return YTDLP


def set_app_id():
    """Identité Windows distincte (barre des tâches) pour SWΛYZ."""
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("SWAYZ.Downloader")
    except Exception:
        pass


def set_window_icon():
    """Applique icon.ico à la fenêtre + barre des tâches (via l'API Win32)."""
    if not os.path.exists(ICON):
        return
    try:
        hwnd = ctypes.windll.user32.FindWindowW(None, "SWΛYZ")
        if not hwnd:
            return
        hicon = ctypes.windll.user32.LoadImageW(
            None, ICON, 1, 0, 0, 0x00000010 | 0x00000040  # IMAGE_ICON | LR_LOADFROMFILE | LR_DEFAULTSIZE
        )
        if hicon:
            ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 0, hicon)  # WM_SETICON small
            ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 1, hicon)  # WM_SETICON big
    except Exception:
        pass

# force UTF-8 stdout (au cas où)
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
except Exception:
    pass


def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def default_folder():
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    return downloads if os.path.isdir(downloads) else os.path.expanduser("~")


class Api:
    def __init__(self):
        self._window = None
        self._cfg = load_config()
        self._downloading = False
        self._updating = False
        self._last_dir = None

    # ---- mises à jour ----
    def get_version(self):
        return {"app": APP_VERSION, "ytdlp": self._ytdlp_version()}

    def _ytdlp_version(self):
        try:
            flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            out = subprocess.run(
                [ytdlp_path(), "--version"], capture_output=True, text=True,
                creationflags=flags, timeout=15,
            )
            return (out.stdout or "").strip() or "?"
        except Exception:
            return "?"

    def check_update(self):
        """Compare la version yt-dlp locale à la dernière sur GitHub."""
        import urllib.request
        cur = self._ytdlp_version()
        try:
            req = urllib.request.Request(
                "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest",
                headers={"User-Agent": "SWAYZ-Downloader"},
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.load(r)
            latest = (data.get("tag_name") or "").strip()
        except Exception:
            return {"ok": False, "code": "offline"}
        return {"ok": True, "current": cur, "latest": latest,
                "needs": bool(latest) and latest != cur}

    def update_ytdlp(self):
        if self._updating:
            return {"ok": False, "error": "Mise à jour déjà en cours."}
        self._updating = True
        threading.Thread(target=self._do_update_ytdlp, daemon=True).start()
        return {"ok": True}

    def _do_update_ytdlp(self):
        import urllib.request
        url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
        tmp = UPDATED_YTDLP + ".part"
        try:
            self._js("onUpdateProgress", 0, "updating")
            req = urllib.request.Request(url, headers={"User-Agent": "SWAYZ-Downloader"})
            with urllib.request.urlopen(req, timeout=60) as r:
                total = int(r.headers.get("Content-Length") or 0)
                done = 0
                with open(tmp, "wb") as f:
                    while True:
                        chunk = r.read(65536)
                        if not chunk:
                            break
                        f.write(chunk)
                        done += len(chunk)
                        if total:
                            self._js("onUpdateProgress", done / total * 100, "updating")
            os.replace(tmp, UPDATED_YTDLP)
            self._js("onUpdateDone", True, self._ytdlp_version())
        except Exception as e:
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass
            self._js("onUpdateDone", False, str(e))
        finally:
            self._updating = False

    # ---- utilitaires fenêtre ----
    def minimize(self):
        if self._window:
            self._window.minimize()

    def close(self):
        if self._window:
            self._window.destroy()

    def get_config(self):
        return {
            "dest": self._cfg.get("dest", default_folder()),
            "mode": self._cfg.get("mode", "video"),
            "lang": self._cfg.get("lang", ""),
        }

    def set_lang(self, lang):
        self._cfg["lang"] = (lang or "")[:8]
        save_config(self._cfg)
        return {"ok": True}

    def choose_folder(self):
        try:
            start = self._cfg.get("dest", default_folder())
            result = self._window.create_file_dialog(
                webview.FOLDER_DIALOG, directory=start
            )
            if result:
                path = result[0] if isinstance(result, (list, tuple)) else result
                self._cfg["dest"] = path
                save_config(self._cfg)
                return path
        except Exception:
            pass
        return self._cfg.get("dest", default_folder())

    def open_folder(self):
        target = self._last_dir or self._cfg.get("dest", default_folder())
        if target and os.path.isdir(target):
            try:
                os.startfile(target)
            except Exception:
                pass

    # ---- analyse du lien (aperçu interactif) ----
    def analyze(self, url):
        url = (url or "").strip()
        if not url:
            return {"ok": False}
        try:
            cmd = [ytdlp_path(), "--dump-single-json", "--no-playlist",
                   "--no-warnings", "--no-update", url]
            flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            out = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8",
                errors="replace", creationflags=flags, timeout=45,
            )
            if out.returncode != 0 or not out.stdout.strip():
                return {"ok": False, "error": "Lien illisible ou vidéo indisponible."}
            data = json.loads(out.stdout)
            heights = sorted(
                {f.get("height") for f in data.get("formats", []) if f.get("height")},
                reverse=True,
            )
            return {
                "ok": True,
                "title": data.get("title") or "Vidéo",
                "thumbnail": data.get("thumbnail") or "",
                "duration": data.get("duration"),
                "uploader": data.get("uploader") or data.get("channel") or "",
                "extractor": data.get("extractor_key") or "",
                "heights": heights,
            }
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "Analyse trop longue. Réessaie."}
        except Exception:
            return {"ok": False, "error": "Impossible d'analyser ce lien."}

    # ---- téléchargement ----
    def start_download(self, url, mode, dest, quality=0, audio_fmt="mp3"):
        if self._downloading:
            return {"ok": False, "code": "busy"}
        url = (url or "").strip()
        if not url:
            return {"ok": False, "code": "no_link"}
        if not os.path.isdir(dest or ""):
            return {"ok": False, "code": "bad_folder"}

        self._cfg["dest"] = dest
        self._cfg["mode"] = mode
        save_config(self._cfg)

        self._downloading = True
        t = threading.Thread(
            target=self._run, args=(url, dest, mode, quality, audio_fmt),
            daemon=True,
        )
        t.start()
        return {"ok": True}

    def _js(self, fn, *args):
        if not self._window:
            return
        payload = ", ".join(json.dumps(a) for a in args)
        try:
            self._window.evaluate_js(f"window.{fn} && window.{fn}({payload})")
        except Exception:
            pass

    def _build_cmd(self, url, dest, mode, quality=0, audio_fmt="mp3"):
        out_tmpl = os.path.join(dest, "%(title)s.%(ext)s")
        base = [
            ytdlp_path(), "--newline", "--no-playlist", "--no-update",
            "--restrict-filenames", "-o", out_tmpl,
        ]
        if FFMPEG_DIR:
            base += ["--ffmpeg-location", FFMPEG_DIR]
        if mode == "audio":
            af = "wav" if str(audio_fmt).lower() == "wav" else "mp3"
            base += ["-f", "bestaudio/best", "-x", "--audio-format", af]
            if af == "mp3":
                base += ["--audio-quality", "0"]
        else:  # video + son — priorité H.264 (avc1) pour lecture universelle
            try:
                q = int(quality)
            except (TypeError, ValueError):
                q = 0
            if q > 0:
                fmt = (
                    f"bv*[vcodec^=avc1][height<={q}]+ba[ext=m4a]/"
                    f"bv*[vcodec^=avc1][height<={q}]+ba/"
                    f"b[vcodec^=avc1][height<={q}]/"
                    f"bv*[height<={q}]+ba/b[height<={q}]/bv*+ba/b"
                )
            else:
                fmt = (
                    "bv*[vcodec^=avc1]+ba[ext=m4a]/"
                    "bv*[vcodec^=avc1]+ba/"
                    "b[vcodec^=avc1]/bv*+ba/b"
                )
            base += ["-f", fmt, "--merge-output-format", "mp4"]
        base.append(url)
        return base

    def _run(self, url, dest, mode, quality=0, audio_fmt="mp3"):
        pct_re = re.compile(r"([\d.]+)%")
        final_path = None
        try:
            cmd = self._build_cmd(url, dest, mode, quality, audio_fmt)
            flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace", creationflags=flags,
            )
            title_shown = False
            merger_path = extract_path = last_dest = None
            for line in proc.stdout:
                line = line.strip()
                if not line:
                    continue
                if "[download]" in line and "%" in line:
                    m = pct_re.search(line)
                    if m:
                        try:
                            pct = float(m.group(1))
                            self._js("onProgress", pct, "downloading")
                        except Exception:
                            pass
                elif "Merging formats into" in line:
                    self._js("onStatus", "merging")
                    mm = re.search(r'Merging formats into "(.+?)"', line)
                    if mm:
                        merger_path = mm.group(1)
                elif line.startswith("[ExtractAudio] Destination:"):
                    self._js("onStatus", "extracting")
                    extract_path = line.split("Destination:", 1)[1].strip()
                elif line.startswith("[download] Destination:"):
                    last_dest = line.split("Destination:", 1)[1].strip()
                    if not title_shown:
                        title_shown = True
                        self._js("onStatus", "downloading")
            proc.wait()
            final_path = merger_path or extract_path or last_dest
            if proc.returncode != 0:
                self._downloading = False
                self._js("onDone", False, "fail")
                return

            # Compatibilité montage : toujours garantir du H.264
            # (ré-encode seulement si la vidéo n'est pas déjà en h264 — donc
            #  instantané en ≤1080p, conversion auto uniquement pour la 4K AV1)
            if mode != "audio" and final_path:
                self._ensure_h264(final_path)

            self._downloading = False
            self._last_dir = dest
            self._js("onDone", True, "done")
        except FileNotFoundError:
            self._downloading = False
            self._js("onDone", False, "no_ytdlp")
        except Exception:
            self._downloading = False
            self._js("onDone", False, "error")

    def _probe(self, path):
        """Renvoie (codec_video, duree_sec) via ffmpeg -i."""
        try:
            flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            out = subprocess.run([FFMPEG, "-i", path], capture_output=True,
                                 text=True, errors="replace", creationflags=flags).stderr
        except Exception:
            return "", 0.0
        codec = ""
        mv = re.search(r"Video:\s*(\w+)", out)
        if mv:
            codec = mv.group(1).lower()
        dur = 0.0
        md = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", out)
        if md:
            dur = int(md.group(1)) * 3600 + int(md.group(2)) * 60 + float(md.group(3))
        return codec, dur

    def _ensure_h264(self, path):
        """Ré-encode en H.264 si la vidéo n'est pas déjà en h264 (pour le montage)."""
        codec, dur = self._probe(path)
        if not codec or codec == "h264":
            return  # déjà compatible, rien à faire
        self._js("onStatus", "reencoding")
        self._js("onProgress", 0, "reencoding")
        tmp = path + ".h264.mp4"
        cmd = [
            FFMPEG, "-y", "-i", path,
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            "-progress", "pipe:1", "-nostats", tmp,
        ]
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                text=True, errors="replace", creationflags=flags,
            )
            for line in proc.stdout:
                line = line.strip()
                if line.startswith("out_time_ms=") and dur > 0:
                    try:
                        ms = int(line.split("=", 1)[1])
                        pct = min(99.0, (ms / 1_000_000.0) / dur * 100.0)
                        self._js("onProgress", pct, "reencoding")
                    except Exception:
                        pass
            proc.wait()
            if proc.returncode == 0 and os.path.isfile(tmp):
                os.replace(tmp, path)
            else:
                try:
                    os.remove(tmp)
                except Exception:
                    pass
        except Exception:
            try:
                if os.path.isfile(tmp):
                    os.remove(tmp)
            except Exception:
                pass


def main():
    set_app_id()
    api = Api()
    window = webview.create_window(
        "SWΛYZ",
        INDEX,
        js_api=api,
        width=470,
        height=780,
        min_size=(430, 640),
        frameless=True,
        easy_drag=False,
        background_color="#08090c",
    )
    api._window = window
    # applique l'icône une fois la fenêtre affichée
    threading.Timer(1.0, set_window_icon).start()

    # hook de test (n'affecte pas l'usage normal) : SWAYZ_TEST=<url>
    test_url = os.environ.get("SWAYZ_TEST")
    if test_url:
        audio_mode = os.environ.get("SWAYZ_TEST_AUDIO")
        def _selftest():
            js = "document.getElementById('link').value=%s; doAnalyze(%s);" % (
                json.dumps(test_url), json.dumps(test_url))
            if audio_mode:
                js += " setMode('audio');"
            if os.environ.get("SWAYZ_TEST_UPDATE"):
                js += " checkUpdate();"
            try:
                window.evaluate_js(js)
            except Exception:
                pass
        threading.Timer(3.5, _selftest).start()

    webview.start()


if __name__ == "__main__":
    main()
