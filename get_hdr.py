import browser_cookie3
import json
import hashlib
import time

def get_sapisid_hash(sapisid, origin="https://music.youtube.com"):
    """Tạo SAPISIDHASH hợp lệ từ SAPISID và origin."""
    timestamp = str(int(time.time()))
    auth_string = f"{timestamp} {sapisid} {origin}"
    sapisid_hash = hashlib.sha1(auth_string.encode()).hexdigest()
    return f"{timestamp}_{sapisid_hash}"

def get_youtube_music_headers():
    try:
        # Lấy cookie từ trình duyệt (Firefox, Chrome)
        cookies = browser_cookie3.firefox(domain_name="youtube.com") or browser_cookie3.chrome(domain_name="youtube.com")

        if not cookies:
            raise ValueError("❌ Không tìm thấy cookie! Hãy đăng nhập vào YouTube Music trước.")

        cookies_dict = {cookie.name: cookie.value for cookie in cookies}

        # Lấy SAPISID từ cookie
        sapisid = cookies_dict.get("SAPISID")
        if not sapisid:
            raise ValueError("❌ Không tìm thấy SAPISID. Đăng nhập lại vào YouTube Music.")

        # Tạo SAPISIDHASH
        authorization = get_sapisid_hash(sapisid)

        # Tạo headers chuẩn
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Referer": "https://music.youtube.com/",
            "X-Goog-AuthUser": "0",
            "X-Youtube-Client-Name": "67",
            "X-Youtube-Client-Version": "1.20250204.03.00",
            "Authorization": f"SAPISIDHASH {authorization}",
            "Cookie": "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
        }

        # Lưu vào file headers_auth.json
        with open("headers_auth.json", "w") as f:
            json.dump(headers, f, indent=4)

        print("✅ headers_auth.json đã được tạo thành công!")
    except Exception as e:
        print("❌ Lỗi khi lấy headers:", e)

if __name__ == "__main__":
    get_youtube_music_headers()
