import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "tracks.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            genre TEXT,
            bpm INTEGER CHECK(bpm > 0),
            duration_sec INTEGER CHECK(duration_sec > 0),
            daw TEXT,
            track_key TEXT
        )
        '''
    )
    conn.commit()

    total = cursor.execute("SELECT COUNT(*) AS total FROM tracks").fetchone()["total"]
    if total == 0:
        demo_tracks = [
            ("Nightfall", "Unirazze", "pluggnb", 140, 185, "FL Studio", "C# minor"),
            ("Digital Tears", "Unirazze", "Archivecore", 165, 142, "FL Studio", "F minor"),
            ("Sunset Bounce", "Max", "ambient", 120, 210, "Ableton", "A major")
        ]
        cursor.executemany(
            '''
            INSERT INTO tracks (title, artist, genre, bpm, duration_sec, daw, track_key)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            demo_tracks
        )
        conn.commit()

    conn.close()