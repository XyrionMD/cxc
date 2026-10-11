"""Shared configuration loader for CodeX Core (cxc).

Configuration lives in ``~/.config/cxc/config.toml``. When upgrading from an
older release that used ``~/.config/cxc/config.py``, the old file is read once
and automatically migrated to TOML (a ``config.py.bak`` backup is kept).
"""

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    raise SystemExit(
        "[!] CodeX Core needs Python 3.11+ (tomllib). Please upgrade Python."
    )

from pathlib import Path
from types import SimpleNamespace

CONFIG_DIR = Path.home() / ".config" / "cxc"
CONFIG_FILE = CONFIG_DIR / "config.toml"
LEGACY_FILE = CONFIG_DIR / "config.py"
LEGACY_LOCK = CONFIG_DIR / ".lock"

REQUIRED_KEYS = {
    "API": "PASTE_YOUR_API_KEY",
    "MODEL": "gemini-2.5-flash",
    "AI_NAME": "Your_Ai_Name",
    "AI_PROMPT": "You Are {AI_NAME}",
    "MUSIC_DIR": "Music",
    "VIDEO_DIR": "Videos",
}


def _escape(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def _render_toml(data):
    def line(key):
        return f'{key} = "{_escape(data.get(key, REQUIRED_KEYS[key]))}"'

    return "\n".join([
        "# CodeX Core (cxc) configuration",
        "# Edit this file then restart cxc.",
        "",
        "# --- AI credentials ---",
        line("API"),
        line("MODEL"),
        line("AI_NAME"),
        "# AI_PROMPT may reference other keys, e.g. {AI_NAME}",
        line("AI_PROMPT"),
        "",
        "# --- Folders (relative to your home directory) ---",
        line("MUSIC_DIR"),
        line("VIDEO_DIR"),
        "",
    ])


def _write_config(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(_render_toml(data), encoding="utf-8")
    try:
        CONFIG_FILE.chmod(0o600)
    except OSError:
        pass


def _migrate_legacy():
    import importlib.util

    spec = importlib.util.spec_from_file_location("cxc_legacy_config", LEGACY_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    legacy = module.Config

    data = {key: str(getattr(legacy, key, default))
            for key, default in REQUIRED_KEYS.items()}

    # Turn the resolved prompt back into a template so it keeps following AI_NAME.
    ai_name = data["AI_NAME"]
    if ai_name and ai_name in data["AI_PROMPT"]:
        data["AI_PROMPT"] = data["AI_PROMPT"].replace(ai_name, "{AI_NAME}")

    _write_config(data)

    try:
        LEGACY_FILE.rename(LEGACY_FILE.with_name("config.py.bak"))
    except OSError:
        pass
    try:
        LEGACY_LOCK.unlink()
    except OSError:
        pass

    print(f"[+] Migrated legacy config -> {CONFIG_FILE}")


def load_config():
    """Return the config as a simple object with attribute access."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        if LEGACY_FILE.exists():
            _migrate_legacy()
        else:
            _write_config(dict(REQUIRED_KEYS))
            print(f"[+] Created config at {CONFIG_FILE}")

    try:
        with CONFIG_FILE.open("rb") as handle:
            data = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise SystemExit(f"[!] Invalid config: {CONFIG_FILE}\n    {exc}")

    for key, default in REQUIRED_KEYS.items():
        data.setdefault(key, default)

    # Resolve simple placeholders (e.g. "{AI_NAME}") inside AI_PROMPT.
    if isinstance(data.get("AI_PROMPT"), str):
        try:
            data["AI_PROMPT"] = data["AI_PROMPT"].format(**data)
        except (KeyError, IndexError, ValueError):
            pass

    return SimpleNamespace(**data)
