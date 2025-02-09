import os
import sys
from unidecode import unidecode

def sanitize_filename(filename):
    """Convert Vietnamese characters to ASCII and replace spaces with underscores."""
    name, ext = os.path.splitext(filename)
    sanitized_name = unidecode(name).replace(" ", "_")
    return f"{sanitized_name}{ext}"

def rename_files_in_directory(directory):
    """Rename all files in a given directory to remove Vietnamese characters."""
    try:
        for filename in os.listdir(directory):
            new_filename = sanitize_filename(filename)
            if filename != new_filename:
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} → {new_filename}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rename_vietnamese_files.py /path/to/directory")
    else:
        rename_files_in_directory(sys.argv[1])
