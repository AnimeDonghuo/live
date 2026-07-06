import re
import os

def sanitize_filename(filename: str) -> str:
    # Prevent path traversal and remove weird characters
    filename = os.path.basename(filename)
    return re.sub(r'[^\w\.\-]', '_', filename)

def format_bytes(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"
