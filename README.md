# 🎵 YouTube Music Liked Songs Downloader

Download your liked songs from YouTube Music as MP3 files, with filenames sanitized for compatibility.

---

## 🛠️ Environment Setup

### 1. Install Python & Pip

Make sure you have **Python 3.8+** and `pip` installed:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Install Required Python Packages

Install all dependencies:

```bash
pip install yt-dlp unidecode tqdm browser-cookie3 ytmusicapi
```

### 3. Get Your YouTube Music Cookies

To access your liked songs, you need to export your YouTube Music cookies:

- **For Firefox:** [Cookie Quick Manager](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/)
- **For Chrome:** [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/)

**Steps:**
1. Log in to [YouTube Music](https://music.youtube.com) in your browser.
2. Use the extension to export cookies for `music.youtube.com`.
3. Save the file as `cookies.txt` and place it in your project directory.

---

## 🚀 Usage

### 1. Run the Main Script

The main script is [`dlp.py`](dlp.py):

```bash
python dlp.py
```

- This will:
  - Update `yt-dlp` to the latest version.
  - Fetch your liked songs list.
  - Download each song as an MP3 into a dated folder under `/home/luan/music/`.
  - Sanitize filenames to remove Vietnamese characters and spaces.

### 2. Check Your Music

Downloaded MP3 files will be in a subfolder of `/home/luan/music/` named with the current date and time.

> **Note:**  
> You should change the `SAVE_PATH` variable in `dlp.py` to your preferred music folder if you want

---

## 📝 Other Scripts

- [`convert_vietnames.py`](convert_vietnames.py): Standalone script to sanitize filenames in a directory.
- [`get_hdr.py`](get_hdr.py): Script to generate `headers_auth.json` for advanced API usage.
- [`mp3_from_ytb.py`](mp3_from_ytb.py): Alternative approach using `ytmusicapi` and `yt-dlp`.

---

## ✅ Features

- Fetches all liked songs from your YouTube Music account.
- Downloads audio as MP3.
- Skips already downloaded songs.
- Handles unavailable videos gracefully.
- Cleans up filenames for compatibility.

---

## ℹ️ Notes

- Make sure your `cookies.txt` is up to date if you change your YouTube login or clear browser cookies.
- If you want to change the download location, edit the `SAVE_PATH` variable in [`dlp.py`](dlp.py).

---

Enjoy your music collection offline! 🎶🚀
