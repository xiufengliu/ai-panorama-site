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
        # Create comments table
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
        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
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

def delete_comment(comment_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        conn.commit()
    finally:
        conn.close()        


def add_message(name, email, message):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )
        conn.commit()
    finally:
        conn.close()

def delete_message(message_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        conn.commit()
    finally:
        conn.close()

def get_messages():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages ORDER BY timestamp DESC")
        return cursor.fetchall()
    finally:
        conn.close()