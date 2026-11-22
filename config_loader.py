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

import os, subprocess, shutil, sys, re
from pathlib import Path
from types import SimpleNamespace
from colors import C
from textual.theme import BUILTIN_THEMES

CONFIG_DIR = Path.home() / ".config" / "cxc"
CONFIG_FILE = CONFIG_DIR / "config.toml"
LEGACY_FILE = CONFIG_DIR / "config.py"
LEGACY_LOCK = CONFIG_DIR / ".lock"

REQUIRED_KEYS = {
    "API": "PASTE_YOUR_API_KEY",
    "MODEL": "gemini-2.5-flash",
    "AI_NAME": "Your_Ai_Name",
    "AI_PROMPT": "You Are {AI_NAME}",
    "LOADING_STYLES": "#",
    "THEME": "catppuccin-mocha",
    "DEBUG": False,
    "MUSIC_DIR": "Music",
    "VIDEO_DIR": "Videos",
}


def _escape(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def _render_toml(data):
    def line(key):
        val = data.get(key, REQUIRED_KEYS[key])
        if isinstance(val, bool):
            return f'{key} = {"true" if val else "false"}'
        if isinstance(val, (int, float)):
            return f'{key} = {val}'
        return f'{key} = "{_escape(str(val))}"'
                                                                

    return "\n".join([
        "# CodeX Core (cxc) configuration",
        "# Edit this file then restart cxc.",
        "",
        "[ai]",
        line("API"),
        line("MODEL"),
        line("AI_PROMPT"),
        "",
        "[appearance]",
        line("LOADING_STYLES"),
        line("AI_NAME"),
        line("THEME"),
        "",
        "[settings]",
        line("DEBUG"),
        "",
        "[folders]",
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
            raw = tomllib.load(handle)
            data = {}
            for k, v in raw.items():
                data.update(v) if isinstance(v, dict) else data.update({k: v})
    except tomllib.TOMLDecodeError as exc:
        return SimpleNamespace(**REQUIRED_KEYS,_broken=True, _error=exc)

    for key, default in REQUIRED_KEYS.items():
        data.setdefault(key, default)

    # Resolve simple placeholders (e.g. "{AI_NAME}") inside AI_PROMPT.
    if isinstance(data.get("AI_PROMPT"), str):
        try:
            data["AI_PROMPT"] = data["AI_PROMPT"].format(**data)
        except (KeyError, IndexError, ValueError):
            pass

    return SimpleNamespace(**data)

def config_reset():
    _write_config(dict(REQUIRED_KEYS))
    print("Config has been reset")

def config_path():
    print("Config Directory...")
    print(CONFIG_DIR)

def config_edit():
    path = CONFIG_DIR / "config.toml"
    candidates = (
        os.environ.get("EDITOR"),
        "nano",
        "vim",
        "nvim",
        "vi"
    )
    for editor in candidates:
        if editor and shutil.which(editor):
            subprocess.run([editor, str(path)])
            return

    print("No editor found! install nano or set $EDITOR")
    print(f"Edit Manual: {path}")
        
    
def conf_fallback(config, args):
    if not getattr(config, "_broken", False):
        return
    match args:
        case ["config", "reset"]:
            config_reset()
            sys.exit(0)
        case ["config", "edit"]:
            config_edit()
            sys.exit(0)
        case _:
            print(f"[!] Invalid config: {CONFIG_FILE}\n    {config._error}")
            print("""[+] Run 'cxc config edit' to fix it, or 'cxc config reset' to reset all settings to default.

Warning: All your settings will be lost, including the API key inside it. Please back up before resetting. """)
            sys.exit(1)
            

def load_state():
    cfg = load_config()
    api_val = getattr(cfg, "API", "")
    return (
        f"{C.GREEN}Active{C.RESET}"
        if api_val and api_val != "PASTE_YOUR_API_KEY"
        else f"{C.RED}API_KEY Not Set{C.RESET}"
        )


def _format_value(old_val: str, new_val: str) -> str:
    old_clean = old_val.strip()

    if old_clean.startswith(('"', "'")):
        escaped = new_val.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'

    if old_clean.lower() in ("true", "false"):
        return new_val.lower()

    if old_clean.isdigit():
        return new_val

    escaped = new_val.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"''"'"'"

def set_conf(key: str, raw_value: str) -> tuple[bool, str]:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        value = f.read()
    pattern = rf"^(\s*{re.escape(key)}\s*=\s*)(.*)$"

    new_value, count = re.subn(
        pattern,
        lambda m: f"{m.group(1)}{_format_value(m.group(2), raw_value)}",
        value,
        count=1,
        flags=re.MULTILINE
    )

    if count == 0:
        return False, f"Key '{key}' not found in configuration."

    new_value = re.sub(r" +$", "", new_value, flags=re.MULTILINE)

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(new_value)

        return True, f"Updated '{key}' to '{raw_value}'"

def list_theme():
    print("Textual Theme List:")
    for i, name in enumerate(BUILTIN_THEMES.keys(), 1):
        print(f"{i}. {name}")

    print("\nTo change the theme, use:\n `cxc config edit`,\n `cxc config set THEME <theme-name>`.")


def debug_mode(*args):
    debug = load_config()
    if (debug.DEBUG) == True:
        print("Debug mode enable")
        print("[Error]:",*args)
    else:
        print("Debug mode is disabled. Enable it in the config file if needed.")
    
