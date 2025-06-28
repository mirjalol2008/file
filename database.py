import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Foydalanuvchilar jadvali
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'uz',
            used_storage INTEGER DEFAULT 0,
            is_paid INTEGER DEFAULT 0,
            premium_until INTEGER DEFAULT 0
        )
    """)
    # Fayllar jadvali
    c.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_name TEXT,
            file_size INTEGER,
            file_path TEXT
        )
    """)
    # Cheklar jadvali
    c.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            photo_path TEXT,
            is_approved INTEGER DEFAULT 0,
            created_at INTEGER
        )
    """)
    conn.commit()
    conn.close()

def add_user_if_not_exists(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def set_user_language(user_id: int, lang: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))
    conn.commit()
    conn.close()

def get_user_language(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else "uz"

def get_user_storage(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT used_storage FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def increase_user_storage(user_id: int, size: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET used_storage = used_storage + ? WHERE user_id = ?", (size, user_id))
    conn.commit()
    conn.close()

def add_file(user_id: int, file_name: str, file_size: int, file_path: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO files (user_id, file_name, file_size, file_path) VALUES (?, ?, ?, ?)",
              (user_id, file_name, file_size, file_path))
    conn.commit()
    conn.close()

def get_user_files(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, file_name, file_size FROM files WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_file_path(file_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT file_path FROM files WHERE id = ?", (file_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def delete_file(file_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM files WHERE id = ?", (file_id,))
    conn.commit()
    conn.close()

def add_payment(user_id: int, photo_path: str, created_at: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO payments (user_id, photo_path, created_at) VALUES (?, ?, ?)",
              (user_id, photo_path, created_at))
    conn.commit()
    conn.close()

def get_unapproved_payments():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, user_id, photo_path, created_at FROM payments WHERE is_approved = 0")
    rows = c.fetchall()
    conn.close()
    return rows

def approve_payment(payment_id: int, extra_storage: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # To'lov tasdiqlanmoqda
    c.execute("UPDATE payments SET is_approved = 1 WHERE id = ?", (payment_id,))
    # Premium saqlash hajmi oshirilmoqda
    # Bu yerda premium_until va used_storage yangilanishi kerak (vaqti kelib qo'shish mumkin)
    conn.commit()
    conn.close()