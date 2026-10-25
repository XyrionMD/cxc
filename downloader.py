import yt_dlp, io, contextlib, time, os, requests
from colors import C
from pathlib import Path

from config_loader import load_config

CVT = load_config()

MUSIC_DIR = Path.home() / CVT.MUSIC_DIR
VIDEO_DIR = Path.home() / CVT.VIDEO_DIR

def SilentLogger():
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        pass

class QuietYDL(yt_dlp.YoutubeDL):
    def to_screen(self, *args, **kwargs):
        pass

    def report_warning(self, *args, **kwargs):
        pass

    def report_error(self, message, *args, **kwargs):
        raise yt_dlp.utils.DownloadError(message)

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'logger': SilentLogger(),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': str(MUSIC_DIR / '%(title)s.%(ext)s'),
}

def search(query):
   try:
       with QuietYDL(ydl_opts) as ydl:
           with contextlib.redirect_stderr(io.StringIO()):
               info = ydl.extract_info(f"ytsearch1:{query}", download=False)

               entries = info.get("entries") or []

               if not entries:
                 print("No results found")
                 return
               else:
                    print("Target Found\n")

               video = info['entries'][0]
               nameC = video.get('uploader')
               duration = video.get('duration')
               description = video.get('description')[:50]
               xcv = info['entries'][0]['title']
               minute, second = divmod(duration, 60)
               print(f"{C.BLUE}Title: {xcv}{C.RESET}")
               print(f"{C.BLUE}Channel: {nameC}{C.RESET}")
               print(f"{C.GREEN}Video Duration: {minute}:{second}{C.RESET}")
               print(f"{C.GREEN}Short description: {description}{C.RESET}")
   except yt_dlp.utils.DownloadError:
         print("Connection Timeout")


def local_search(query):
    try:
        from rapidfuzz import fuzz
    except ImportError:
        fuzz = None

    query = query.strip().lower()

    if not query:
        print("Please provide a keyword to search")
        return

    tokens = query.split()
    folders = [MUSIC_DIR, VIDEO_DIR]
    matches = []

    for folder in folders:
        if not folder.exists():
            continue

        for file in folder.rglob("*"):
            if not file.is_file():
                continue

            name = file.stem.lower()
            score = 0

            for tok in tokens:
                if len(tok) < 3 or fuzz is None:
                    if tok not in name:
                        score = 0
                        break
                    score = max(score, 100)
                else:
                    ratio = fuzz.partial_ratio(tok, name)
                    if ratio < 70:
                        score = 0
                        break
                    score = max(score, ratio)

            if score:
                matches.append((score, file))

    if not matches:
        print(f'No local file matching "{query}"')
        return

    matches.sort(key=lambda item: item[0], reverse=True)

    print(f"Found {len(matches)} local file(s):\n")
    for score, file in matches:
        print(f"  {C.GREEN}{file.name}{C.RESET} {C.BLUE}[{score:.0f}%]{C.RESET}")
        print(f"      {C.CYAN}{file}{C.RESET}")


def download(query):
   print("Please Wait...")

   time.sleep(1)
   try:
       with QuietYDL(ydl_opts) as ydl:
           with contextlib.redirect_stderr(io.StringIO()):
               info = ydl.extract_info(f"ytsearch1:{query}", download=False)

               entries = info.get("entries") or []

               if not entries:
                  print("No results found")
                  return
               else:
                    print("Target Found, Starting Download")

               Xid = info['entries'][0]['id']
               url = f"https://youtu.be/{Xid}"
               xcv = info['entries'][0]['title']

               with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                   ydl.download([url])
               print(f"Downloaded: {xcv}")
               print("Play it with mpx: cxc mpx")

   except yt_dlp.utils.DownloadError:
        print("Connection Timeout")
        return

def video_dowloader(query, quality):
    options = f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"

    opts = {
        'format': options,
        'quiet': True,
        'no_warnings': True,
        'logger': SilentLogger(),
        'merge_output_format': 'mp4',
        'outtmpl': str(VIDEO_DIR / '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([query])

    except yt_dlp.utils.DownloadError:
        print("Connection Timeout")
        return

def update_OTA(Version):
    url = "https://pypi.org/pypi/cxc/json"

    try:
        respon = requests.get(url)
        respon.raise_for_status()

        data_json = respon.json()
        new_version = data_json['info']['version']

        if Version == new_version:
            print("Latest version:" ,Version)
        else:
            print("Update Avaible Version:" ,new_version)
            cmd = input("Update now?[y/n]").lower().strip()
            if cmd == "y":
                print("Please Wait...")
                time.sleep(1)
                os.system("pipx upgrade cxc")
            else:
                print("aborted.")

    except requests.exceptions.RequestException:
        print("Failed to fetch latest version from PyPI. Please check your internet connection.")
