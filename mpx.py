import os, time, subprocess
from pathlib import Path

from config_loader import load_config

CVT = load_config()

MUSIC_DIR = Path.home() / CVT.MUSIC_DIR

mpv_state = None

def mpx():
  global mpv_state
  
  
  while True:
    try:
      os.system("clear")
      print("Welcome To Music Player X")
      cmd = input("MPX >>> ").lower().strip()

      if cmd == "quit":
        return

      elif cmd.startswith("play "):
        args = cmd.split(" ", 1)[1]
        songs = sorted(MUSIC_DIR.glob("*.mp3")) + sorted(MUSIC_DIR.glob("*.flac")) + sorted(MUSIC_DIR.glob("*.wav"))

        if args == "all":
          if mpv_state:
            mpv_state.terminate()
          print("[+] Playing All Songs")

          cmd_args = ["mpv", "--no-video"] + [str(s) for s in songs]
          mpv_state = subprocess.Popen(cmd_args)
          
        if not songs:
          print("[-] Empty Music Folder ")
        elif args.isdigit():
            idx = int(args) - 1
            if 0 <= idx < len(songs):
              song = songs[idx]
              if mpv_state:
                mpv_state.terminate()

              print(f"[+] Playing: {song.name}")
              mpv_state = subprocess.Popen(["mpv", "--no-video", str(song)])
            else:
                print(f"[-] Number {args} not found. Max: {len(songs)}")
        else:
            song = MUSIC_DIR / args
            if song.exists():
              if mpv_state:
                mpv_state.terminate()
              print(f"[+] Playing: {song.name}")
              mpv_state = subprocess.Popen(["mpv", "--no-video", str(song)])
            else:
                print(f"[-] File {args} not found ")
        input()
      elif cmd == "list":
        songs = sorted(MUSIC_DIR.glob("*.mp3")) + sorted(MUSIC_DIR.glob("*.flac")) + sorted(MUSIC_DIR.glob("*.wav"))
        if not songs:
          print("[-]Empty Music Folder ")
        else:
            print("=" * 56)
            for i, song in enumerate(songs, 1):
              print(f"{i}. {song.name}")
            print("play all, for play all music in folder")
            print("=" * 56)
            print("Enter To Exit")
            input()
      elif cmd == "help":
        print("""
======================
Avaible Command:
======================
- play <args>
- list
- help



[NOTES]
When running inside this interactive shell,
mpv controls may experience input buffering delay.
If shortcuts like Space (Pause) or q (Stop) feel unresponsive, 
please press the key 2-3 times consecutively to trigger it.
Enter To Exit
        """)
        input()
      
    except Exception as e:
      printf("Error: {e}")