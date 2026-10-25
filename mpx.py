import os
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse, unquote

from config_loader import load_config

CVT = load_config()

MUSIC_DIR = Path.home() / CVT.MUSIC_DIR

AUDIO_EXT = (".mp3", ".flac", ".wav", ".m4a", ".ogg")

# python-vlc loads the native libvlc library on import, which may be missing.
try:
    import vlc
except Exception:
    vlc = None


def _get_tracks():
    if not MUSIC_DIR.exists():
        return []
    return sorted(
        (p for p in MUSIC_DIR.iterdir()
         if p.is_file() and p.suffix.lower() in AUDIO_EXT),
        key=lambda p: p.name.lower(),
    )


def _mrl_name(mrl):
    if not mrl:
        return None
    if mrl.startswith("file://"):
        return Path(unquote(urlparse(mrl).path)).name
    return mrl


class VlcBackend:
    """Playback through python-vlc (full controls)."""

    name = "vlc"

    def __init__(self):
        self.instance = vlc.Instance()
        if self.instance is None:
            raise RuntimeError("libvlc not available")
        self.list_player = self.instance.media_list_player_new()
        self.media_player = self.list_player.get_media_player()
        self.tracks = []

    def play(self, tracks, start=0):
        self.tracks = list(tracks)
        playlist = self.instance.media_list_new([str(t) for t in self.tracks])
        self.list_player.set_media_list(playlist)
        self.list_player.play_item_at_index(start)

    def stop(self):
        self.list_player.stop()

    def toggle_pause(self):
        self.media_player.pause()

    def resume(self):
        self.media_player.set_pause(0)
        if not self.list_player.is_playing():
            self.list_player.play()

    def next(self):
        self.list_player.next()

    def previous(self):
        self.list_player.previous()

    def set_volume(self, value):
        self.media_player.audio_set_volume(value)

    def get_volume(self):
        return self.media_player.audio_get_volume()

    def is_playing(self):
        return bool(self.list_player.is_playing())

    def current_name(self):
        media = self.media_player.get_media()
        if media is None:
            return None
        return _mrl_name(media.get_mrl())

    def close(self):
        try:
            self.list_player.stop()
        except Exception:
            pass


class MpvBackend:
    """Fallback playback through the mpv binary (limited controls)."""

    name = "mpv"

    def __init__(self):
        if shutil.which("mpv") is None:
            raise RuntimeError("mpv not found")
        self.process = None
        self.tracks = []
        self.current = None

    def play(self, tracks, start=0):
        self.tracks = list(tracks)
        self.stop()
        args = ["mpv", "--no-video"] + [str(t) for t in self.tracks[start:]]
        self.process = subprocess.Popen(
            args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        self.current = self.tracks[start].name if self.tracks[start:] else None

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
        self.process = None
        self.current = None

    def is_playing(self):
        return self.process is not None and self.process.poll() is None

    def current_name(self):
        return self.current if self.is_playing() else None

    def _unsupported(self, what):
        print(f"[-] {what} is not supported with the mpv fallback")

    def toggle_pause(self):
        self._unsupported("Pause/resume")

    def resume(self):
        self._unsupported("Resume")

    def next(self):
        self._unsupported("Next")

    def previous(self):
        self._unsupported("Previous")

    def set_volume(self, value):
        self._unsupported("Volume")

    def get_volume(self):
        return 100

    def close(self):
        self.stop()


def _build_backend():
    if vlc is not None:
        try:
            return VlcBackend()
        except Exception as exc:
            print(f"[!] VLC unavailable ({exc}); falling back to mpv")
    if shutil.which("mpv"):
        return MpvBackend()
    return None


def _status_line(backend):
    name = backend.current_name()
    return f"[{name}] " if name else ""


def _print_tracks(tracks):
    print("=" * 56)
    for i, song in enumerate(tracks, 1):
        print(f"{i}. {song.name}")
    print("=" * 56)
    print(f"{len(tracks)} track(s). Use 'play <n>' or 'play all'.")


HELP_TEXT = """
======================
 Available Commands
======================
- play <n>        : play track number <n>
- play all        : play every track in the folder
- play <filename> : play a file by name
- pause           : pause / resume
- resume          : resume playback
- stop            : stop playback
- next / prev     : next / previous track
- volume <0-100>  : set volume (no argument shows current)
- now             : show the current track
- list            : list all tracks
- help            : show this help
- quit            : exit mpx
"""


def _handle_play(backend, tracks, arg):
    if not tracks:
        print("[-] Empty Music Folder")
        return
    if not arg:
        print("Usage: play <n> | play all | play <filename>")
        return
    if arg.lower() == "all":
        backend.play(tracks, start=0)
        print(f"[+] Playing all ({len(tracks)} track(s))")
        return
    if arg.isdigit():
        idx = int(arg) - 1
        if 0 <= idx < len(tracks):
            backend.play(tracks, start=idx)
            print(f"[+] Playing: {tracks[idx].name}")
        else:
            print(f"[-] Number {arg} not found. Max: {len(tracks)}")
        return
    match = next((t for t in tracks if t.name == arg), None)
    if match is None:
        match = next((t for t in tracks if arg.lower() in t.name.lower()), None)
    if match is None:
        print(f"[-] File {arg} not found")
        return
    backend.play([match], start=0)
    print(f"[+] Playing: {match.name}")


def _handle_volume(backend, arg):
    if not arg:
        print(f"[+] Volume: {backend.get_volume()}")
        return
    try:
        value = int(arg)
    except ValueError:
        print("[-] Volume must be a number 0-100")
        return
    value = max(0, min(100, value))
    backend.set_volume(value)
    print(f"[+] Volume set to {value}")


def mpx():
    backend = _build_backend()
    if backend is None:
        print("[-] No audio backend found. Install VLC (libvlc) or mpv.")
        return

    os.system("clear")
    print("Welcome To Music Player X")
    if backend.name == "mpv":
        print("[!] Using mpv fallback - pause/next/prev/volume are limited")
    print("Type 'help' for commands.\n")

    while True:
        tracks = _get_tracks()
        try:
            cmd = input(f"MPX {_status_line(backend)}>>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            backend.close()
            return

        low = cmd.lower()

        if low in ("quit", "exit", "q"):
            backend.close()
            return

        if low in ("help", "h"):
            print(HELP_TEXT)
            input("Enter To Exit")
            os.system("clear")
        elif low in ("list", "ls"):
            if not tracks:
                print("[-] Empty Music Folder")
            else:
                _print_tracks(tracks)
            input("Enter To Exit")
            os.system("clear")
        elif low == "now":
            name = backend.current_name()
            print(f"[+] Now playing: {name}" if name else "[-] Nothing is playing")
            input("Enter To Exit")
        elif low.startswith("play"):
            _handle_play(backend, tracks, cmd[4:].strip())
            input("Enter To Exit")
            os.system("clear")
        elif low == "pause":
            backend.toggle_pause()
        elif low == "resume":
            backend.resume()
        elif low == "stop":
            backend.stop()
        elif low == "next":
            backend.next()
        elif low in ("prev", "previous"):
            backend.previous()
        elif low.startswith("volume"):
            _handle_volume(backend, cmd[len("volume"):].strip())
        elif low.startswith("vol"):
            _handle_volume(backend, cmd[len("vol"):].strip())
        elif not low:
            continue
        else:
            print(f"[-] Unknown command: {cmd} (type 'help')")
