import os
import json
from ytmusicapi import YTMusic
import yt_dlp

# Đường dẫn để lưu MP3
SAVE_PATH = "/home/luan/music"  # Thay đổi đường dẫn này

# Khởi tạo YouTube Music API
ytmusic = YTMusic("headers_auth.json")  # Cần file headers_auth.json

def get_liked_playlist():
    from ytmusicapi import YTMusic
    ytmusic = YTMusic("headers_auth.json")  # Kiểm tra file này có hợp lệ không

    raw_response = ytmusic.get_liked_songs(limit=1000)  # Lấy dữ liệu

    print("Raw response:", raw_response)  # Debug xem có dữ liệu không

    if not raw_response:  # Nếu phản hồi rỗng hoặc None
        raise ValueError("API returned an empty response")

    return raw_response

def download_song(video_id, title, save_path):
    """Tải xuống một bài hát từ YouTube bằng yt-dlp."""
    output_template = os.path.join(save_path, f"{title}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "extract_audio": True,
        "audio_format": "mp3",
        "outtmpl": output_template,
        "quiet": False,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://music.youtube.com/watch?v={video_id}"])

def main():
    os.makedirs(SAVE_PATH, exist_ok=True)

    print("Đang lấy danh sách bài hát đã thích...")
    liked_songs = get_liked_playlist()

    for song in liked_songs:
        title = song["title"].replace("/", "_")  # Tránh lỗi tên file
        video_id = song["videoId"]
        if video_id:
            print(f"Tải xuống: {title}")
            download_song(video_id, title, SAVE_PATH)
        else:
            print(f"Bỏ qua {title} (không có video ID)")

if __name__ == "__main__":
    main()
