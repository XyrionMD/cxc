# CodeX Core (cxc)

[![PyPI version](https://img.shields.io/pypi/v/cxc.svg)](https://pypi.org/project/cxc)
[![Python Version](https://img.shields.io/pypi/pyversions/cxc.svg)](https://pypi.org/project/cxc)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-XyrionMD%2Fcxc-blue.svg)](https://github.com/XyrionMD/cxc)

A feature-rich command-line tool for music/video downloading, local media management, AI chat, and interactive playback — all in one lightweight package.

**GitHub:** https://github.com/XyrionMD/cxc  
**PyPI:** https://pypi.org/project/cxc

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎵 **Music Search & Download** | Search YouTube and download audio as MP3 (192 kbps) |
| 🎬 **Video Downloader (DV)** | Download videos at chosen resolutions (e.g., 360p, 720p, 1080p) |
| 🔍 **Local Search** | Find downloaded files with fuzzy/typo-tolerant matching |
| 🎧 **mpx (Music Player X)** | Interactive TUI player with VLC backend (full controls) and mpv fallback |
| 🤖 **AI Chat** | Terminal-based chat UI powered by Google Gemini API (Textual TUI) |
| ⏰ **Time Utility** | Display current time, day, month, and year |
| 🔄 **Self Update** | Checks PyPI for latest version and upgrades via `pipx` |
| ⚙️ **TOML Config** | Clean `~/.config/cxc/config.toml` with auto-migration from legacy `config.py` |

---

## 📦 Installation

### Via pipx (Recommended)
```bash
pipx install cxc
```

### Via pip
```bash
pip install cxc
```

> **Requirements:** Python 3.11+, `ffmpeg` (for audio conversion), and optionally `libvlc` (for full mpx controls) or `mpv` (fallback).

---

## 🚀 Quick Start

```bash
# First run creates config at ~/.config/cxc/config.toml
cxc help

# Set your Gemini API key for chat
nano ~/.config/cxc/config.toml

# Search and download music
cxc download "your favorite song"

# Play it with mpx
cxc mpx
```

---

## 📖 Commands Reference

| Command | Alias | Description |
|---------|-------|-------------|
| `cxc search "<title>"` | `-S` | Search YouTube for music info |
| `cxc search --local "<title>"` | | Search downloaded files locally (fuzzy) |
| `cxc download "<title>"` | `-D` | Search and download music as MP3 |
| `cxc DV -r "<res>" "<URL>"` | | Download video at resolution (e.g., `360`, `720`, `1080`) |
| `cxc mpx` | | Open Music Player X (interactive) |
| `cxc chat` | | Open AI chat (requires API key in config) |
| `cxc time` | `-t` | Show current time, day, month, year |
| `cxc update` | `-U` | Check PyPI and upgrade via `pipx` |
| `cxc version` | `-v` | Show current version |
| `cxc help` | `h` | Display help menu |

---

## 🎧 mpx — Music Player X

`cxc mpx` launches an interactive music player. It prefers **python-vlc** (full controls: pause, next/prev, volume) and falls back to **mpv** (play/stop only) if libvlc isn't available.

### mpx Commands

| Command | Description |
|---------|-------------|
| `play <n>` | Play track number `n` |
| `play all` | Play all tracks in order |
| `play <filename>` | Play a specific file by name |
| `pause` / `resume` | Pause or resume playback |
| `stop` | Stop playback |
| `next` / `prev` | Next or previous track |
| `volume <0-100>` | Set volume (no argument shows current) |
| `now` | Show currently playing track |
| `list` / `ls` | List all tracks |
| `help` / `h` | Show help |
| `quit` / `q` | Exit mpx |

> **Note:** Install `vlc` (with `libvlc` headers) for the best experience. On Debian/Ubuntu: `sudo apt install vlc libvlc-dev`. On Arch: `sudo pacman -S vlc`.

---

## 🤖 AI Chat

`cxc chat` opens a beautiful Textual TUI for chatting with Google Gemini.

### Setup

1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Edit `~/.config/cxc/config.toml`:
   ```toml
   API = "your-gemini-api-key"
   MODEL = "gemini-2.5-flash"   # or your preferred model
   AI_NAME = "CodeX"
   AI_PROMPT = "You Are {AI_NAME}"
   ```
3. Run `cxc chat`

### Chat Controls
- **Type message + Enter** — Send
- **`quit`** — Exit chat
- **`help`** / **Ctrl+H** — Show help modal
- **Ctrl+Q** — Quit immediately

---

## ⚙️ Configuration

Config file: `~/.config/cxc/config.toml` (created automatically on first run, permissions `600`).

```toml
# CodeX Core (cxc) configuration
# Edit this file then restart cxc.

# --- AI credentials ---
API = "PASTE_YOUR_API_KEY"
MODEL = "gemini-2.5-flash"
AI_NAME = "Your_Ai_Name"
# AI_PROMPT may reference other keys, e.g. {AI_NAME}
AI_PROMPT = "You Are {AI_NAME}"

# --- Folders (relative to your home directory) ---
MUSIC_DIR = "Music"
VIDEO_DIR = "Videos"
```

| Key | Description |
|-----|-------------|
| `API` | Gemini API key (required for `cxc chat`) |
| `MODEL` | AI model to use (e.g., `gemini-2.5-flash`) |
| `AI_NAME` | Display name for the AI in chat |
| `AI_PROMPT` | System prompt; can reference `{AI_NAME}` |
| `MUSIC_DIR` | Folder for downloaded music (relative to `$HOME`) |
| `VIDEO_DIR` | Folder for downloaded videos (relative to `$HOME`) |

### Migration from Old Versions

If you're upgrading from a version that used `~/.config/cxc/config.py`, cxc automatically:
1. Reads the old `config.py`
2. Writes the new `config.toml`
3. Backs up the old file as `config.py.bak`
4. Removes the legacy `.lock` file

Your API key and settings are preserved.

---

## 🔄 Self Update

```bash
cxc update
# or
cxc -U
```

Checks PyPI for the latest version. If a newer version exists, prompts to run `pipx upgrade cxc`.

---

## 📋 Requirements

| Dependency | Purpose |
|------------|---------|
| Python 3.11+ | Core runtime (requires `tomllib`) |
| `yt-dlp` | Video/audio downloading |
| `ffmpeg` | Audio conversion to MP3 |
| `python-vlc` + `libvlc` | Full-featured mpx backend (recommended) |
| `mpv` | Fallback mpx backend |
| `textual` | TUI for AI chat |
| `requests` | HTTP requests (AI chat, update check) |
| `rapidfuzz` | Optional: faster fuzzy local search |

Install system dependencies:
```bash
# Debian/Ubuntu
sudo apt install ffmpeg vlc libvlc-dev mpv

# Arch
sudo pacman -S ffmpeg vlc mpv

# Fedora
sudo dnf install ffmpeg vlc vlc-devel mpv
```

---

## 📁 Project Structure

```
cxc/
├── cxc.py           # Main entry point & command dispatch
├── downloader.py    # Search, download, video download, local search, update
├── chat.py          # AI chat TUI (Textual + Gemini API)
├── mpx.py           # Music Player X (VLC/mpv backends)
├── config_loader.py # TOML config with legacy migration
├── colors.py        # ANSI color constants
├── pyproject.toml   # Packaging metadata
├── LICENSE          # MIT License
└── README.md        # This file
```

---

## 📝 Changelog

### v1.1.0 (Current)
- Smarter `cxc update`: checks PyPI and only prompts when a newer version exists
- Download now hands off to `cxc mpx` instead of spawning separate mpv
- Code cleanup: removed unused imports and leftover mpv playback code

### v1.0.0 (First Stable Release)
- Video Downloader (DV) with resolution selection
- Self-update via `pipx`
- Local search with fuzzy matching
- Config migration from `config.py` → `config.toml`
- VLC-based mpx with full playback controls
- Modern `pyproject.toml` packaging

> **Note:** Versions `1.26.x` were the nightly channel. **v1.0.0 is the first stable release**, so versioning restarts from here.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

Copyright (c) 2026 [Xyrion](https://github.com/XyrionMD)

---

## 👤 Author

**Rion (XyrionMD)**  
GitHub: [@XyrionMD](https://github.com/XyrionMD)  
PyPI: [cxc](https://pypi.org/project/cxc)

---

<p align="center">
  Made with boredom and Python 🐍
</p>