#!/bin/python3
import sys, datetime

from pathlib import Path

from colors import C
from config_loader import load_config, config_path, config_edit, config_reset, conf_fallback, set_conf, list_theme
from downloader import search, download, video_dowloader, update_OTA, local_search
from mpx import mpx

CVT = load_config()

arg = sys.argv[1:]

MUSIC_DIR = Path.home() / CVT.MUSIC_DIR
MUSIC_DIR.mkdir(parents=True, exist_ok=True)

VIDEO_DIR = Path.home() / CVT.VIDEO_DIR
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

Version = "2.0.1"


def show_help():
    print(f"""
=================================================
CodeX Core <==> cxc
=================================================

Version: {Version}

Usage: cxc <commands> [options]

Available commands :
- search <title> / -S <title>    : Search Music Information 
- search --local <title>         : Search your downloaded files locally
- download <title> / -D <title>  : Search and download music to MP3 
- time                           : Displays time, day, month, year 
- chat                           : Open the chat menu with AI 
- mpx                            : Music Player X
- DV                             : Video Downloader
- state                          : Display current system state
- about                          : Show information about cxc
- config                         : Manage cxc Configuration
- update                         : Self Update 
- version / -v                   : Show Version
- help / h                       : Display this help menu 
          """)

def show_help_download():
    print("""
=======================================
Download Help 
=======================================
- cxc download "<Music Title>"

 [cxc download --help / -h]
""")

def show_help_DV():
    print("""
=======================================
DV Help    
=======================================
- cxc DV -r "reso" "<URL Video>"
    

# Example
- cxc DV -r "360" "https://youtube.com/xXxxX"  
    

[cxc DV --help / -h]
""")

def show_help_play():
    print("""
=======================================
mpx Help
=======================================
cxc mpx

 [cxc mpx --help / -h]
""")

def show_help_chat():
    print("""
=======================================
How To Use cxc chat?
=======================================
step 1 
settings up your config
- nano ~/.config/cxc/config.toml

last step
open cxc chat
- cxc chat

 [cxc chat --help / -h]
""")

def show_about():
    print("""
========================================
   CodeX Core (CXC)
   AI & Media Tools for Your Terminal
========================================

Created by : Rion (Xyrion)
License    : MIT License
PyPI       : https://pypi.org/project/cxc
Github     : https://github.com/XyrionMD/cxc

About:
CXC is an all-in-one CLI utility born out of boredom, built to bring 
music/video downloading (yt-dlp), terminal audio playback (mpx), and 
Gemini AI chat right into your command line.

Type 'cxc help' to explore available commands.
""")

def show_help_config(invalid_cmd=None):
    if invalid_cmd:
        print("Subcommands:", invalid_cmd, "not found. \n")
    print("""
======================================
cxc Help Config
======================================

Usage: cxc config <commands>

Available Commands:
- reset      : Reset configuration
- path       : Show your path config
- edit       : Edit configuration
- set        : Set a configuration value
- list-theme : List available themes

Examples:
    cxc config path
    cxc config edit
    cxc config reset
    cxc config set <KEY> <VALUE>
    cxc config list-theme
""")

def show_help_search():
    print('cxc search "<Music title>"')
    print('cxc search --local "<Music title>"')
    print("\n [cxc search --help / -h]")

cvt = datetime.datetime.now()

def show_time():
    print("Day:", cvt.strftime("%A"))
    print("Hours:", cvt.strftime("%H:%M:%S"))
    print("Month:", cvt.strftime("%B %Y"))

def main():
    conf_fallback(CVT, [a.lower() for a in sys.argv[1:]])
    from statelib import state
    from chat import askAI
    match arg:
        case ["download"] | ["-D"] | ["download", "--help"] | ["download", "-h"]:
            show_help_download()

        case ["download", query] | ["-D", query]:
            download(query)

        case ["DV"] | ["DV", "--help"] | ["DV", "-h"]:
            show_help_DV()

        case ["DV", "-r", quality, query]:
            video_dowloader(query, quality)

        case ["update"] | ["-U"]:
            update_OTA(Version)

        case ["mpx", "--help"] | ["mpx", "-h"]:
            show_help_play()
                

        case ["mpx"]:
            mpx()

        case ["help"] | ["--help"] | ["h"] | ["-h"]:
            show_help()

        case ["time"] | ["-t"]:
            show_time()

        case ["search"] | ["-S"] | ["search", "--help"] | ["search", "-h"]:
            show_help_search()

        case ["search", "--local", query]:
            local_search(query)

        case ["search",query] | ["-S", query]:
            search(query)

        case ["chat", "--help"] | ["chat", "-h"]:
            show_help_chat()

        case ["chat"]:
            askAI()

        case ["state"]:
            print(state())

        case ["about"]:
            show_about()

        case ["config"]  | ["config", "help" ] | ["config","--help"]:
            show_help_config()

        case ["config", "path"]:
            config_path()

        case ["config", "edit"]:
            config_edit()

        case ["config", "reset"]:
            config_reset()

        case ["config", "set", key, value]:
            success, message = set_conf(key, value)
            print(message)

        case ["config", "list-theme"]:
            list_theme()

        case ["config", "set", *missing]:
            show_help_config()

        case ["config", unknown,  *rest]:
            show_help_config(invalid_cmd=unknown)
            
        case ["version"] | ["-v"]:
            print("CodeX Core" ,Version)

        case []:
            show_help()

        case _:
            print("Command Not Found")
            show_help()


if __name__ == "__main__":
    main()


