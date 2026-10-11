#!/bin/python3

import sys, datetime, shutil, subprocess

from pathlib import Path

from colors import C
from config_loader import load_config
from chat import askAI
from downloader import search, download, video_dowloader, update_OTA, local_search
from mpx import mpx

CVT = load_config()

arg = sys.argv[1:]

mpv_process = None

MUSIC_DIR = Path.home() / CVT.MUSIC_DIR
MUSIC_DIR.mkdir(parents=True, exist_ok=True)

VIDEO_DIR = Path.home() / CVT.VIDEO_DIR
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

Version = "1.0.0 Stable"


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
    global mpv_process
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
            update_OTA()

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

        case ["version"] | ["-v"]:
            print(Version)

        case []:
            show_help()

        case _:
            print("Command Not Found")
            show_help()


