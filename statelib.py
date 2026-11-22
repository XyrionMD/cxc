import shutil, platform, os, tomllib, stat, sys
from pathlib import Path
from colors import C
from config_loader import load_config, load_state

CF = load_config()

MUSIC = Path.home() / CF.MUSIC_DIR

CONFDIR = Path.home() / ".config/cxc/config.toml"

p = Path(CONFDIR)
xfz = p.stat()
mode = xfz.st_mode

venv_path = os.getenv("VIRTUAL_ENV")
is_venv = venv_path is not None and sys.prefix != sys.base_prefix

py_bin = f"{C.BLUE}{sys.executable}{C.RESET}"
py_ver = f"{sys.version_info.major}-{sys.version_info.minor}-{sys.version_info.micro}"

if is_venv:
    venv_state = f"venv ({C.BLUE}{venv_path}{C.RESET})"
else:
    venv_state = "system"

xfgz = oct(mode & 0o777)
state_mode = f"{C.GREEN}Secure{C.RESET}" if xfgz == "0o600" else f"{C.YELLOW}Warning{C.RESET}"


def state():
    try:
        apikey_state = load_state()
        distro = platform.freedesktop_os_release()
        name = (distro.get("PRETTY_NAME",distro.get("NAME", "Unknown")))
        ID = (distro.get("ID"))
    except OSError:
        name = platform.system()
        ID = "Unknown"

    kernel = platform.release()

    ffmpeg = f"{C.GREEN}Installed{C.RESET}" if shutil.which("ffmpeg") is not None else f"{C.RED}ffmpeg Not Installed{C.RESET}"

    if MUSIC.is_dir():
        folder_state = str(MUSIC)
    else: 
        folder_state = "Music folder not found. Configure it in ~/.config/cxc/config.toml."

    return (
        "===========================================\n"
        "CXC STATE...\n"
        "===========================================\n"
        f"Distro      : {C.CYAN}{name}{C.RESET}\n"
        f"ID          : {C.CYAN}{ID}{C.RESET}\n"
        f"Kernel      : {C.CYAN}{kernel}{C.RESET}\n"
        f"FFmpeg      : {ffmpeg}\n"
        f"APIKEY      : {apikey_state}\n"
        f"Python3     : {py_bin} ({py_ver})\n"
        f"Env         : {venv_state}\n"
        f"Config Mode : {xfgz} ({state_mode})\n"
        f"Config DIR  : {C.BLUE}{CONFDIR}{C.RESET}\n"   
        f"Music  DIR  : {C.BLUE}{folder_state}{C.RESET}"
    )

