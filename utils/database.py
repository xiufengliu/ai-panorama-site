import sqlite3

def create_db():
    conn = sqlite3.connect("aibook.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            comment TEXT,
            parent_id INTEGER DEFAULT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

def add_comment(name, email, comment, parent_id=None):
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments (name, email, comment, parent_id) VALUES (?, ?, ?, ?)",
        (name, email, comment, parent_id),
    )
    conn.commit()
    conn.close()

def get_comments(parent_id=None):
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()
    if parent_id is None:
        cursor.execute("SELECT * FROM comments WHERE parent_id IS NULL ORDER BY timestamp DESC")
    else:
        cursor.execute(
            "SELECT * FROM comments WHERE parent_id = ? ORDER BY timestamp ASC", (parent_id,)
        )
    comments = cursor.fetchall()
    conn.close()
    return comments