import sqlite3
from pathlib import Path

DB_NAME = "aibook.db"
DB_PATH = Path(__file__).parent / DB_NAME

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                comment TEXT NOT NULL,
                parent_id INTEGER DEFAULT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES comments (id)
            )
        """)
        conn.commit()
    finally:
        conn.close()

def get_comments(parent_id=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if parent_id is None:
            cursor.execute("SELECT * FROM comments WHERE parent_id IS NULL ORDER BY timestamp DESC")
        else:
            cursor.execute("SELECT * FROM comments WHERE parent_id = ? ORDER BY timestamp ASC", (parent_id,))
        return cursor.fetchall()
    finally:
        conn.close()

def add_comment(name, email, comment, parent_id=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO comments (name, email, comment, parent_id) VALUES (?, ?, ?, ?)",
            (name, email, comment, parent_id)
        )
        conn.commit()
    finally:
        conn.close()