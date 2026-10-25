**CodeX Core CXC**

Hello everyone, my name is Rion. This is my boredom project, which might be useful for you. This tool has several features such as:

**Features**

- Download Music with yt-dlp
- Search Music with yt-dlp
- Video Downloader (DV)
- Local Search
- mpx Music Player X (VLC / mpv)
- AI Chat
- Self Update (checks PyPI, upgrades via pipx)

**How to use**

```
cxc help
```

**Commands**

| Command                        | Alias | Description                          |
| ------------------------------ | ----- | ------------------------------------ |
| `cxc search "<title>"`         | `-S`  | Search music information             |
| `cxc search --local "<title>"` |       | Search your downloaded files locally |
| `cxc download "<title>"`       | `-D`  | Search and download music to MP3     |
| `cxc DV -r "<res>" "<URL>"`    |       | Download a video at a chosen quality |
| `cxc mpx`                      |       | Open Music Player X                  |
| `cxc chat`                     |       | Open the AI chat menu                |
| `cxc time`                     | `-t`  | Show time, day, month, and year      |
| `cxc update`                   | `-U`  | Check PyPI and update via `pipx`     |
| `cxc version`                  | `-v`  | Show the current version             |
| `cxc help`                     | `h`   | Display the help menu                |

**mpx (Music Player X)**

`cxc mpx` opens an interactive player. It uses **python-vlc** when available and automatically falls back to **mpv** otherwise.

| Command           | Description                       |
| ----------------- | --------------------------------- |
| `play <n>`        | Play track number `<n>`           |
| `play all`        | Play every track in the folder    |
| `play <filename>` | Play a file by name               |
| `pause`           | Pause / resume                    |
| `resume`          | Resume playback                   |
| `stop`            | Stop playback                     |
| `next` / `prev`   | Next / previous track             |
| `volume <0-100>`  | Set volume (no argument shows it) |
| `now`             | Show the current track            |
| `list`            | List all tracks                   |
| `help`            | Show the mpx help                 |
| `quit`            | Exit mpx                          |

> Note: python-vlc needs the native **libvlc** library. On systems without it, `cxc mpx` falls back to **mpv** (with limited controls: no pause/next/prev/volume).

**Configuration**

cxc stores its settings in `~/.config/cxc/config.toml` (TOML format). The file is created automatically on first run — just edit it and restart cxc.

```toml
# CodeX Core (cxc) configuration

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

| Key         | Description                                                       |
| ----------- | ----------------------------------------------------------------- |
| `API`       | Your Gemini API key (required for `cxc chat`).                    |
| `MODEL`     | The AI model to use, e.g. `gemini-2.5-flash`.                     |
| `AI_NAME`   | The name shown for the AI in chat.                                |
| `AI_PROMPT` | The system prompt. May reference other keys, e.g. `{AI_NAME}`.    |
| `MUSIC_DIR` | Folder for downloaded music, relative to your home directory.     |
| `VIDEO_DIR` | Folder for downloaded videos, relative to your home directory.    |

**Config format & migration**

The configuration format changed from a Python file (`config.py`) to **TOML** (`config.toml`). You don't need to do anything manually:

- If you upgrade from an old version, cxc migrates automatically the first time you run it:
  1. reads your old `config.py`,
  2. writes the new `config.toml`,
  3. keeps a backup of the old file as `config.py.bak`,
  4. removes the old `.lock` file.
- Your API key and all other settings are preserved.
- If you have no old config, a fresh `config.toml` is created for you.
- The file is stored with owner-only permissions (`600`) because it holds your API key.
- cxc now requires **Python 3.11+** (for the built-in `tomllib`).

**Update**

## What's New in v1.1.0

- **Smarter `cxc update`** — the updater now checks PyPI for the latest release and only offers to upgrade when a newer version exists, instead of always running `pipx upgrade`.
- **Download hands off to mpx** — after a download finishes, cxc prints the saved track name and points you to `cxc mpx` to play it, instead of spawning a separate mpv player.
- **Cleanup** — removed leftover mpv playback code and unused imports from `cxc.py`, `downloader.py`, and `chat.py`.

## What's New in v1.0.0 (First Stable Release)

- **Video Downloader (DV)** — download videos with yt-dlp and pick the resolution, e.g. `cxc DV -r "360" "<URL>"`.
- **Self Update** — update cxc straight from the terminal using `pipx upgrade`, e.g. `cxc update`.
- **Local Search** — find your downloaded music/videos on your device with partial-title and typo-tolerant matching, e.g. `cxc search --local "<music title>"`.
- **New config format** — configuration moved from `config.py` to `config.toml`, with automatic migration from the old file. See the [Configuration](#configuration) section.
- **VLC-based mpx** — the music player now uses `python-vlc` with full playback controls (pause, next/prev, volume), with an automatic `mpv` fallback.
- **pyproject.toml** — packaging moved from `setup.py` to the modern `pyproject.toml` standard.

**Notes**

- Before using the chat feature, please set your configuration first in `~/.config/cxc/config.toml` (see [Configuration](#configuration)).
- The current stable release is **v1.1.0**.
- The `1.26.x` versions were the **nightly** channel. **v1.0.0 is the first stable release** of CXC, so the versioning restarts from here.

I will update regularly but I can't guarantee it, so see you in the next update.
