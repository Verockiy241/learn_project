from .database import get_connection

def get_all_tracks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tracks ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_track_by_id(track_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tracks WHERE id = ?", (track_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

# Функция для получения списка уникальных жанров из базы
def get_all_genres():
    conn = get_connection()
    # Берем только уникальные названия, чтобы в списке не было повторов
    rows = conn.execute(
        "SELECT DISTINCT genre FROM tracks WHERE genre IS NOT NULL AND genre != '' ORDER BY genre"
    ).fetchall()
    conn.close()
    return [row["genre"] for row in rows]

def create_track(track_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO tracks (title, artist, genre, bpm, duration_sec, daw, track_key)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            track_data["title"],
            track_data["artist"],
            track_data.get("genre"),
            track_data.get("bpm"),
            track_data.get("duration_sec"),
            track_data.get("daw"),
            track_data.get("track_key")
        )
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_track_by_id(new_id)

def update_track(track_id: int, track_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE tracks
        SET title = ?, artist = ?, genre = ?, bpm = ?, duration_sec = ?, daw = ?, track_key = ?
        WHERE id = ?
        ''',
        (
            track_data["title"],
            track_data["artist"],
            track_data.get("genre"),
            track_data.get("bpm"),
            track_data.get("duration_sec"),
            track_data.get("daw"),
            track_data.get("track_key"),
            track_id
        )
    )
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    return get_track_by_id(track_id) if updated_rows > 0 else None

def delete_track(track_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tracks WHERE id = ?", (track_id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    return deleted_rows > 0

def delete_multiple_tracks(track_ids: list[int]):
    if not track_ids:
        return 0
    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ','.join('?' for _ in track_ids)
    cursor.execute(f"DELETE FROM tracks WHERE id IN ({placeholders})", track_ids)
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    return deleted_rows