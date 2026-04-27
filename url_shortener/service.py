import string
from db import get_connection

BASE62 = string.ascii_letters + string.digits

def encode(num):
    base = len(BASE62)
    res = []
    while num:
        res.append(BASE62[num % base])
        num //= base
    return ''.join(reversed(res)) or '0'

def get_or_create_short_url(long_url):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Try inserting directly
        cursor.execute("INSERT INTO urls (long_url) VALUES (?)", (long_url,))
        url_id = cursor.lastrowid

        short_code = encode(url_id)

        cursor.execute(
            "UPDATE urls SET short_code = ? WHERE id = ?",
            (short_code, url_id)
        )

        conn.commit()
        return short_code

    except Exception:
        # If already exists, fetch existing
        cursor.execute("SELECT short_code FROM urls WHERE long_url = ?", (long_url,))
        row = cursor.fetchone()
        return row[0] if row else None

    finally:
        conn.close()

def get_long_url(short_code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
