import sqlite3

def get_connection():
    return sqlite3.connect("urls.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        long_url TEXT UNIQUE,
        short_code TEXT UNIQUE
    )
    """)
    conn.commit()
    conn.close()
