import os

def test_environment():
    print("\033[1;34mTesting environment variables and basic functionality...\033[0m")

    # Test if SAVE_PATH exists
    save_path = os.getenv('SAVE_PATH', '/home/luan/music')
    if os.path.exists(save_path):
        print(f"\033[1;32mSAVE_PATH exists: {save_path}\033[0m")
    else:
        print(f"\033[1;31mSAVE_PATH does not exist: {save_path}\033[0m")

    # Test if COOKIES_FILE exists
    cookies_file = os.getenv('COOKIES_FILE', 'cookies.txt')
    if os.path.exists(cookies_file):
        print(f"\033[1;32mCOOKIES_FILE exists: {cookies_file}\033[0m")
    else:
        print(f"\033[1;31mCOOKIES_FILE does not exist: {cookies_file}\033[0m")

    # Test if yt-dlp is installed
    yt_dlp_installed = os.system("which yt-dlp > /dev/null 2>&1") == 0
    if yt_dlp_installed:
        print("\033[1;32myt-dlp is installed\033[0m")
    else:
        print("\033[1;31myt-dlp is not installed\033[0m")

if __name__ == "__main__":
    test_environment()