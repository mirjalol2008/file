from database import get_user_storage
from config import FREE_LIMIT_BYTES

def check_user_limit(user_id: int, file_size: int) -> bool:
    current_used = get_user_storage(user_id)
    if current_used + file_size > FREE_LIMIT_BYTES:
        return False
    return True

def format_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f}{size_name[i]}"