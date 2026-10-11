# CodeX Core (cxc)

[![PyPI Version](https://img.shields.io/pypi/v/cxc.svg)](https://pypi.org/project/cxc/)
[![Python Version](https://img.shields.io/pypi/pyversions/cxc.svg)](https://pypi.org/project/cxc/)
[![License](https://img.shields.io/github/license/XyrionMD/Cxc)](LICENSE)

**CodeX Core (cxc)** is a powerful command-line toolkit that brings AI-powered utilities, media downloading, and playback capabilities directly to your terminal. Built for developers and power users who want a unified, keyboard-driven workflow.

---

## Features

| Feature | Command | Description |
|---------|---------|-------------|
| **Music Search** | `cxc search` / `cxc -S` | Search YouTube for music and view metadata |
| **Local Search** | `cxc search --local` | Fuzzy-search your downloaded music/video library |
| **Music Download** | `cxc download` / `cxc -D` | Download audio from YouTube as high-quality MP3 |
| **Video Download** | `cxc DV` | Download videos with selectable resolution |
| **Music Player X (mpx)** | `cxc mpx` | Interactive terminal music player with playlist support |
| **AI Chat** | `cxc chat` | Terminal-based chat with Google Gemini models |
| **Time Display** | `cxc time` / `cxc -t` | Show current day, time, and month |
| **Self Update** | `cxc update` / `cxc -U` | Upgrade cxc to the latest version via pipx |

---

## Requirements

- **Python 3.11+** (uses `tomllib` from standard library)
- **mpv** — media player backend for audio/video playback
- **ffmpeg** — required by yt-dlp for audio extraction and merging
- **pipx** — recommended installation method (isolated environment)

### Install System Dependencies

**Debian/Ubuntu:**
```bash
sudo apt update && sudo apt install python3.11 python3.11-venv mpv ffmpeg pipx
```

**Arch Linux:**
```bash
sudo pacman -S python mpv ffmpeg pipx
```

**Fedora:**
```bash
sudo dnf install python3.11 mpv ffmpeg pipx
```

**macOS (Homebrew):**
```bash
brew install python@3.11 mpv ffmpeg pipx
```

Ensure `pipx` is in your PATH:
```bash
pipx ensurepath
# Restart your shell or run: source ~/.bashrc (or ~/.zshrc)
```

---

## Installation

### Recommended: Install with pipx (Latest Stable Release)

```bash
pipx install cxc
```

This installs `cxc` in an isolated environment and makes the `cxc` command globally available.

> **Note:** Releases are published to **PyPI first**. The GitHub repository may not immediately reflect the latest PyPI version. For the latest stable release, always prefer `pipx install cxc`.

### Alternative: Install from GitHub (Development / Bleeding Edge)

```bash
pipx install git+https://github.com/XyrionMD/Cxc.git
```

> **Warning:** This tracks the GitHub source which may be *behind* the latest PyPI release (since source is pushed after publishing). Use this only for testing unreleased changes or contributing.

### Verify Installation

```bash
cxc --help
cxc -v
```

---

## First-Time Setup

After installation, run `cxc` once to generate the default configuration:

```bash
cxc
```

This creates `~/.config/cxc/config.toml` with placeholder values. You **must** edit it before using AI chat or download features:

```bash
nano ~/.config/cxc/config.toml
```

### Configuration Options

```toml
# CodeX Core (cxc) configuration
# Edit this file then restart cxc.

# --- AI credentials ---
API = "PASTE_YOUR_GEMINI_API_KEY"
MODEL = "gemini-2.5-flash"
AI_NAME = "Your_Ai_Name"
AI_PROMPT = "You Are {AI_NAME}"

# --- Folders (relative to your home directory) ---
MUSIC_DIR = "Music"
VIDEO_DIR = "Videos"
```

| Key | Description | Required |
|-----|-------------|----------|
| `API` | Your Google Gemini API key ([Get one here](https://aistudio.google.com/apikey)) | **Yes** (for chat) |
| `MODEL` | Gemini model to use (e.g., `gemini-2.5-flash`, `gemini-2.5-pro`) | **Yes** (for chat) |
| `AI_NAME` | Display name for the AI in chat | No (default: `Your_Ai_Name`) |
| `AI_PROMPT` | System prompt; can reference `{AI_NAME}` | No |
| `MUSIC_DIR` | Folder under `$HOME` for downloaded music | No (default: `Music`) |
| `VIDEO_DIR` | Folder under `$HOME` for downloaded videos | No (default: `Videos`) |

> **Note:** The config file is automatically created with secure permissions (`600`). Your API key is stored locally only.

---

## Usage Guide

### General Help

```bash
cxc --help
cxc -h
```

### Search Music (Online)

```bash
cxc search "song title"
cxc -S "song title"
```

Shows title, channel, duration, and short description.

### Search Local Library

```bash
cxc search --local "query"
```

Fuzzy-searches filenames in `~/Music` and `~/Videos` using RapidFuzz.

### Download Music (MP3)

```bash
cxc download "song title"
cxc -D "song title"
```

Downloads the first YouTube result as 192 kbps MP3 to `~/Music`. Prompts to play after download.

### Download Video

```bash
cxc DV -r "720" "https://youtube.com/watch?v=..."
```

- `-r` / `--resolution`: Target height (e.g., `360`, `480`, `720`, `1080`)
- Saves to `~/Videos` as MP4

### Music Player X (mpx)

```bash
cxc mpx
```

Interactive shell with commands:

| Command | Action |
|---------|--------|
| `list` | Show all songs with numbers |
| `play <number>` | Play song by index |
| `play <filename>` | Play by exact filename |
| `play all` | Play entire library in order |
| `help` | Show mpx help |
| `quit` | Exit mpx |

> **Tip:** Inside mpx, mpv controls (Space=pause, q=quit, ←/→=seek) may need 2–3 keypresses due to input buffering.

### AI Chat

```bash
cxc chat
```

Opens a Textual TUI chat interface powered by Google Gemini.

**Controls:**
- Type message + Enter → Send
- `help` → Show help modal
- `quit` or `Ctrl+Q` → Exit
- `Ctrl+H` → Help modal

Requires valid `API` and `MODEL` in config.

### Show Current Time

```bash
cxc time
cxc -t
```

### Check Version

```bash
cxc version
cxc -v
```

### Self-Update

```bash
cxc update
cxc -U
```

Runs `pipx upgrade cxc` internally. If it fails, you'll be prompted to retry.

---

## Upgrading from Old Versions (Breaking Changes)

**Version 1.0.0 introduces major changes.** If you installed cxc before this release, you **must reinstall** to get the new architecture.

### What Changed?

| Aspect | Old Version | New Version (1.0.0+) |
|--------|-------------|----------------------|
| Config format | `~/.config/cxc/config.py` (Python) | `~/.config/cxc/config.toml` (TOML) |
| Python requirement | 3.8+ | **3.11+** (stdlib `tomllib`) |
| Install method | `pip install` / manual | **pipx only** (recommended) |
| Config migration | Manual | **Automatic** (backups old file) |
| Dependencies | Different set | `requests`, `textual`, `yt-dlp`, `rapidfuzz` |

### Migration Steps for Existing Users

#### 1. Uninstall the Old Version

If you installed via pip:
```bash
pip uninstall cxc
```

If you installed manually (cloned repo):
```bash
# Remove any manually installed scripts or symlinks
# Check ~/.local/bin, /usr/local/bin, etc.
```

#### 2. Remove Old Config (Optional but Recommended)

The new version auto-migrates `config.py` → `config.toml`, but a clean start avoids issues:

```bash
mv ~/.config/cxc/config.py ~/.config/cxc/config.py.old
# The new version will create a fresh config.toml on first run
```

#### 3. Ensure Python 3.11+ is Default

```bash
python3 --version
# Must show 3.11.x or higher
```

If your default `python3` is older, install 3.11+ and ensure it's on PATH.

#### 4. Install Fresh with pipx

```bash
pipx install cxc
# Or from GitHub for absolute latest:
pipx install git+https://github.com/XyrionMD/Cxc.git
```

#### 5. Run Once to Generate New Config

```bash
cxc
```

#### 6. Edit New Config

```bash
nano ~/.config/cxc/config.toml
```

Add your Gemini API key and preferred model.

#### 7. Verify Everything Works

```bash
cxc -v
cxc search "test"
cxc chat
```

---

## Project Structure

```
cxc/
├── cxc.py           # Main entry point, command dispatcher
├── chat.py          # Textual TUI AI chat (Gemini)
├── downloader.py    # YouTube search/download (yt-dlp)
├── mpx.py           # Interactive music player (mpv)
├── config_loader.py # TOML config + legacy migration
├── colors.py        # ANSI color constants
├── setup.py         # Package metadata
└── LICENSE          # MIT License
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP calls to Gemini API |
| `textual` | Terminal UI framework for chat |
| `yt-dlp` | YouTube search & download engine |
| `rapidfuzz` | Fast fuzzy string matching (local search) |
| `tomllib` | TOML parsing (stdlib in Python 3.11+) |

All installed automatically via pipx.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'tomllib'`
**Cause:** Python < 3.11.  
**Fix:** Upgrade to Python 3.11+ and reinstall with pipx.

### `cxc: command not found`
**Cause:** pipx bin directory not in PATH.  
**Fix:** Run `pipx ensurepath` and restart shell.

### `Connection Timeout` on search/download
**Cause:** Network issue or yt-dlp needs update.  
**Fix:** Check internet; optionally run `pipx upgrade cxc` to get latest yt-dlp.

### `mpv` not found / playback fails
**Cause:** mpv not installed.  
**Fix:** Install mpv via your package manager (see Requirements).

### Config migration failed
**Cause:** Corrupt `config.py`.  
**Fix:** Delete `~/.config/cxc/config.py` and `~/.config/cxc/.lock`, then run `cxc` to regenerate.

### AI Chat: "Connection Error" or 400/403
**Cause:** Invalid API key, quota exceeded, or model unavailable.  
**Fix:** Verify API key at [Google AI Studio](https://aistudio.google.com/apikey), check quota, try a different model.

---

## Uninstall

```bash
pipx uninstall cxc
```

To also remove config and data:
```bash
rm -rf ~/.config/cxc
rm -rf ~/Music   # your downloaded music
rm -rf ~/Videos  # your downloaded videos
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push: `git push origin feature-name`
5. Open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) for details.

Copyright (c) 2026 Xyrion

---

## Links

- **GitHub:** https://github.com/XyrionMD/Cxc
- **PyPI:** https://pypi.org/project/cxc/
- **Issues:** https://github.com/XyrionMD/Cxc/issues

---

> **CodeX Core** — Your terminal, supercharged. 🚀