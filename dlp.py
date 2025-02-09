import os
import subprocess
from unidecode import unidecode
import datetime
import sys
import re
from tqdm import tqdm

# --- Ensure yt-dlp is up to date ---
print("\033[1;34m🔹 Updating yt-dlp package to the latest version...\033[0m")
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Create a folder with date and time for this session
now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
SAVE_PATH = f"/home/luan/music/{now}"
COOKIES_FILE = "cookies.txt"  # Ensure this file exists

os.makedirs(SAVE_PATH, exist_ok=True)

def sanitize_filename(filename):
    """Convert Vietnamese characters to ASCII and replace spaces with underscores."""
    name, ext = os.path.splitext(filename)
    sanitized_name = unidecode(name).replace(" ", "_")
    return f"{sanitized_name}{ext}"

print("\033[1;34m🔹 Fetching the list of liked songs...\033[0m")

# Clean the liked_songs.txt file before fetching new music
with open("liked_songs.txt", "w", encoding="utf-8") as file:
    file.truncate(0)

yt_dlp_command = [
    "yt-dlp", "--flat-playlist",
    "--cookies", COOKIES_FILE,
    "--print-to-file", "%(title)s - https://music.youtube.com/watch?v=%(id)s",
    "liked_songs.txt",
    "https://music.youtube.com/playlist?list=LM"
]

# Start yt-dlp and capture output
process = subprocess.Popen(
    yt_dlp_command,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

total = None
pbar = None

for line in process.stdout:
    # Example: [download] Downloading item 3 of 405
    match = re.search(r"\[download\] Downloading item (\d+) of (\d+)", line)
    if match:
        current = int(match.group(1))
        total = int(match.group(2))
        if pbar is None:
            pbar = tqdm(total=total, desc="Fetching playlist", unit="item")
        pbar.n = current
        pbar.refresh()
    # Optionally, suppress or print other lines as needed

if pbar:
    pbar.n = pbar.total
    pbar.refresh()
    pbar.close()

process.wait()

with open("liked_songs.txt", "r", encoding="utf-8") as file:
    songs = file.readlines()

for song in songs:
    parts = song.strip().split(" - https://music.youtube.com/watch?v=")
    if len(parts) != 2:
        print(f"\033[1;31m⚠️ Line format error: {song}\033[0m")
        continue

    title, video_id = parts
    file_name = f"{title}.mp3"
    sanitized_file_name = sanitize_filename(file_name)
    sanitized_file_path = os.path.join(SAVE_PATH, sanitized_file_name)

    # Check if already downloaded in this session's folder
    if os.path.exists(sanitized_file_path):
        print(f"\033[1;32m✅ Already exists: {sanitized_file_name} (Skipping)\033[0m")
        continue

    print(f"\033[1;34m🎵 Downloading: {title}\033[0m")
    output_template = os.path.join(SAVE_PATH, f"{title}.%(ext)s")

    yt_dlp_opts = [
        "yt-dlp", "-f", "bestaudio/best",
        "--cookies", COOKIES_FILE,
        "--extract-audio", "--audio-format", "mp3",
        "--output", output_template,
        "--quiet", "--no-warnings",
        f"https://music.youtube.com/watch?v={video_id}"
    ]

    result = subprocess.run(
        yt_dlp_opts,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    downloaded_file_path = os.path.join(SAVE_PATH, file_name)
    if result.returncode != 0 or not os.path.exists(downloaded_file_path):
        print(f"\033[1;31m⚠️ Error: Video not available ({title}), skipping...\033[0m")
        continue

    # Rename if needed
    if downloaded_file_path != sanitized_file_path:
        os.rename(downloaded_file_path, sanitized_file_path)
        print(f"\033[1;32mRenamed: {file_name} → {sanitized_file_name}\033[0m")
    else:
        print(f"\033[1;32mDownloaded: {sanitized_file_name}\033[0m")

print("\033[1;32m✅ Done! All songs have been downloaded and renamed in the directory:\033[0m", SAVE_PATH)