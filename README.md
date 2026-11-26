# CodeX Core (cxc)

[![PyPI version](https://img.shields.io/pypi/v/cxc.svg)](https://pypi.org/project/cxc)
[![Python Version](https://img.shields.io/pypi/pyversions/cxc.svg)](https://pypi.org/project/cxc)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
| 🎧 **mpx (Music Player X)** | Interactive player with VLC backend (full controls) and mpv fallback |
| 🤖 **AI Chat** | Terminal-based chat UI powered by Google Gemini API (Textual TUI) |
| 🔐 **Private API Requests** | Gemini API key travels in the `x-goog-api-key` header, never in the URL |
| 🖼️ **File & Image to AI** | Send images (JPG/PNG/WebP) or text files to Gemini with `/file` |
| 🎨 **Textual Themes** | Pick a chat theme from Textual's built-in themes, saved automatically |
| 🩺 **System State** | Inspect distro, kernel, FFmpeg, API key, Python/venv and config status |
| 🛠️ **Config CLI** | View, edit, reset and set config values without leaving the terminal |
| 🐞 **Debug Mode** | Optional verbose error output for chat, downloads and update checks |
| ⏰ **Time Utility** | Display current time, day, month, and year |
| 🔄 **Self Update** | Checks PyPI for latest version and upgrades via `pipx` |
| ⚙️ **TOML Config** | Sectioned `~/.config/cxc/config.toml` with auto-migration from legacy `config.py` |

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

# Set your Gemini API key without opening an editor
cxc config set API "your-gemini-api-key"

# Search and download music
cxc download "your favorite song"

# Play it with mpx
cxc mpx

# Check your setup
cxc state
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
| `cxc state` | | Display current system and config state |
| `cxc about` | | Show information about cxc |
| `cxc config <subcommand>` | | Manage configuration (see below) |
| `cxc time` | `-t` | Show current time, day, month, year |
| `cxc update` | `-U` | Check PyPI and upgrade via `pipx` |
| `cxc version` | `-v` | Show current version |
| `cxc help` | `h`, `--help`, `-h` | Display help menu |

> Most commands also accept `--help` / `-h` for a short usage hint, e.g. `cxc download --help`, `cxc DV -h`, `cxc mpx --help`, `cxc chat --help`, `cxc search --help`.

---

## 🛠️ Configuration Management

Use `cxc config` to manage `~/.config/cxc/config.toml` directly:

| Subcommand | Description |
|------------|-------------|
| `cxc config path` | Print the config directory path |
| `cxc config edit` | Open the config in `$EDITOR`, `nano`, `vim`, `nvim`, or `vi` |
| `cxc config reset` | Restore all defaults (⚠️ wipes your API key) |
| `cxc config set <KEY> <VALUE>` | Update a single key in place |
| `cxc config list-theme` | List all available Textual themes |
| `cxc config help` | Show the config help menu |

Examples:

```bash
cxc config set API "AIza..."
cxc config set THEME "dracula"
cxc config set DEBUG true
cxc config list-theme
```

If the TOML file is malformed, cxc won't crash on startup: it prints the parse error and asks you to run `cxc config edit` (fix manually) or `cxc config reset` (restore defaults). Back up your API key before resetting.

---

## 🩺 System State

`cxc state` prints a diagnostic snapshot:

```text
===========================================
CXC STATE...
===========================================
Distro      : Arch Linux
ID          : arch
Kernel      : 6.x.x-arch1-1
FFmpeg      : Installed
APIKEY      : Active
Python3     : /usr/bin/python3 (3-11-9)
Env         : system
Config Mode : 0o600 (Secure)
Config DIR  : /home/you/.config/cxc/config.toml
Music  DIR  : /home/you/Music
```

It reports FFmpeg availability, API key status, Python executable/version, whether you're inside a virtual environment, and whether the config file has secure `600` permissions.

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

> **Note:** Install `vlc` (with `libvlc` headers) for the best experience. The mpv fallback works for play/stop but prints a notice for unsupported controls. On Debian/Ubuntu: `sudo apt install vlc libvlc-dev`. On Arch: `sudo pacman -S vlc`.

---

## 🤖 AI Chat

`cxc chat` opens a Textual TUI for chatting with Google Gemini. Conversations keep their history for the whole session and are sent with your `AI_PROMPT` as the system instruction.

### Setup

1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Edit `~/.config/cxc/config.toml` (or use `cxc config set ...`):
   ```toml
   [ai]
   API = "your-gemini-api-key"
   MODEL = "gemini-2.5-flash"
   AI_PROMPT = "You Are {AI_NAME}"
   ```
3. Run `cxc chat`

> Your API key is sent in the `x-goog-api-key` request header — it is never part of the URL, so connection errors and debug output can't expose it.

### Chat Controls

- **Type message + Enter** — Send
- **`help`** / **Ctrl+H** — Show help modal (**ESC** closes it)
- **`quit`** — Exit chat
- **Ctrl+Q** — Quit immediately

### Sending Files to the AI

Use `/file <path> <prompt>` inside the chat:

```text
/file ~/photo.png What do you see here?
/file ./notes.txt Summarize this for me.
```

- Supported image types: `.jpg`, `.jpeg`, `.png`, `.webp` — sent inline as base64 (vision).
- Other files are read as UTF-8 text and appended to the prompt.
- `~` is expanded automatically; missing files are reported in chat.
- If you omit the prompt, it defaults to `Analyze this file.`

### Appearance & Debugging

- `THEME` sets the Textual theme on startup (default: `catppuccin-mocha`). Changing the theme in-app is saved back to the config automatically. Run `cxc config list-theme` to see valid names.
- `LOADING_STYLES` controls the style of the animated "typing..." indicator (default: `#`).
- `DEBUG = true` prints verbose error details in chat, downloads, and update checks. Leave it off for normal use.

---

## ⚙️ Configuration

Config file: `~/.config/cxc/config.toml` (created automatically on first run, permissions `600`).

Settings are grouped into sections:

```toml
# CodeX Core (cxc) configuration
# Edit this file then restart cxc.

[ai]
API = "PASTE_YOUR_API_KEY"
MODEL = "gemini-2.5-flash"
AI_PROMPT = "You Are {AI_NAME}"

[appearance]
LOADING_STYLES = "#"
AI_NAME = "Your_Ai_Name"
THEME = "catppuccin-mocha"

[settings]
DEBUG = false

[folders]
MUSIC_DIR = "Music"
VIDEO_DIR = "Videos"
```

| Section | Key | Description |
|---------|-----|-------------|
| `[ai]` | `API` | Gemini API key (required for `cxc chat`) |
| `[ai]` | `MODEL` | AI model to use (e.g., `gemini-2.5-flash`) |
| `[ai]` | `AI_PROMPT` | System prompt; can reference `{AI_NAME}` |
| `[appearance]` | `LOADING_STYLES` | Textual style used by the chat typing indicator |
| `[appearance]` | `AI_NAME` | Display name for the AI in chat |
| `[appearance]` | `THEME` | Textual theme name (`cxc config list-theme`) |
| `[settings]` | `DEBUG` | Verbose error output when `true` |
| `[folders]` | `MUSIC_DIR` | Folder for downloaded music (relative to `$HOME`) |
| `[folders]` | `VIDEO_DIR` | Folder for downloaded videos (relative to `$HOME`) |

### Migration from Old Versions

If you're upgrading from a version that used `~/.config/cxc/config.py`, cxc automatically:
1. Reads the old `config.py`
2. Writes the new, sectioned `config.toml` (including default theme/debug values)
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
| `textual` | TUI for AI chat + built-in theme list |
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
├── chat.py          # AI chat TUI (Textual + Gemini API, /file support)
├── mpx.py           # Music Player X (VLC/mpv backends)
├── config_loader.py # Sectioned TOML config, migration, config CLI helpers
├── statelib.py      # System/config state report for `cxc state`
├── colors.py        # ANSI color constants
├── LICENSE          # MIT License
└── README.md        # This file
```

---

## 📝 Changelog

### v2.0.2 (Current)
- Gemini API key now sent via the `x-goog-api-key` header instead of the URL query string, so error messages can't leak it
- Version bumped to `2.0.2`

### v2.0.1
- New `cxc state` command with distro, kernel, FFmpeg, API key, Python/venv and config permission info
- New `cxc config` CLI: `path`, `edit`, `reset`, `set`, `list-theme`
- New `cxc about` command and per-command `--help` hints
- Config moved to sections (`[ai]`, `[appearance]`, `[settings]`, `[folders]`) with new `THEME`, `LOADING_STYLES` and `DEBUG` keys
- Chat: `/file <path> <prompt>` for images (JPG/PNG/WebP) and text files, plus animated typing indicator
- Chat themes are loaded from config and saved back when changed; malformed TOML now shows a recovery hint instead of crashing
- Optional debug mode for verbose errors across chat, downloads and updates

### v1.1.0
- Smarter `cxc update`: checks PyPI and only prompts when a newer version exists
- Download now hands off to `cxc mpx` instead of spawning separate mpv
- Code cleanup: removed unused imports and leftover mpv playback code

### v1.0.0 (First Stable Release)
- Video Downloader (DV) with resolution selection
- Self-update via `pipx`
- Local search with fuzzy matching
- Config migration from `config.py` → `config.toml`
- VLC-based mpx with full playback controls
- Modern packaging

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
