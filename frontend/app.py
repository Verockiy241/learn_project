from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:8000"


def get_int_or_none(val):
    return int(val) if val and val.strip() else None


def fetch_genres():
    """Вспомогательная функция для получения списка жанров из API"""
    try:
        response = requests.get(f"{API_URL}/genres", timeout=5)
        return response.json() if response.ok else []
    except Exception:
        return []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tracks")
def track_list():
    try:
        response = requests.get(f"{API_URL}/tracks", timeout=5)
        tracks = response.json() if response.ok else []
    except Exception:
        tracks = []
    return render_template("list.html", tracks=tracks)


@app.route("/tracks/create", methods=["GET", "POST"])
def create_track():
    if request.method == "POST":
        data = {
            "title": request.form.get("title"),
            "artist": request.form.get("artist"),
            "genre": request.form.get("genre", ""),
            "bpm": get_int_or_none(request.form.get("bpm")),
            "duration_sec": get_int_or_none(request.form.get("duration_sec")),
            "daw": request.form.get("daw", ""),
            "track_key": request.form.get("track_key", "")
        }
        requests.post(f"{API_URL}/tracks", json=data, timeout=5)
        return redirect(url_for("track_list"))

    return render_template("form.html", track=None, genres=fetch_genres())


@app.route("/tracks/<int:track_id>/edit", methods=["GET", "POST"])
def edit_track(track_id: int):
    if request.method == "POST":
        data = {
            "title": request.form.get("title"),
            "artist": request.form.get("artist"),
            "genre": request.form.get("genre", ""),
            "bpm": get_int_or_none(request.form.get("bpm")),
            "duration_sec": get_int_or_none(request.form.get("duration_sec")),
            "daw": request.form.get("daw", ""),
            "track_key": request.form.get("track_key", "")
        }
        requests.put(f"{API_URL}/tracks/{track_id}", json=data, timeout=5)
        return redirect(url_for("track_list"))

    response = requests.get(f"{API_URL}/tracks/{track_id}", timeout=5)
    track_data = response.json() if response.ok else None
    return render_template("form.html", track=track_data, genres=fetch_genres())


@app.route("/tracks/<int:track_id>/delete", methods=["POST"])
def delete_track(track_id: int):
    requests.delete(f"{API_URL}/tracks/{track_id}", timeout=5)
    return redirect(url_for("track_list"))


@app.route("/tracks/bulk_delete", methods=["POST"])
def bulk_delete_tracks():
    """Маршрут для массового удаления выбранных треков"""
    track_ids = request.form.getlist("track_ids")
    if track_ids:
        # Превращаем строковые ID в числа для API
        ids_to_delete = [int(tid) for tid in track_ids]
        requests.post(f"{API_URL}/tracks/bulk-delete", json={"track_ids": ids_to_delete}, timeout=5)
    return redirect(url_for("track_list"))

# Вариант в app.py для добавления "заготовленных" жанров
def fetch_genres():
    default_genres = ["Phonk", "Hyperpop", "Lo-Fi", "Techno"] # Ваши заготовки
    try:
        response = requests.get(f"{API_URL}/genres", timeout=5)
        db_genres = response.json() if response.ok else []
        # Объединяем ваши заготовки и жанры из базы, убирая дубликаты
        return sorted(list(set(default_genres + db_genres)))
    except Exception:
        return default_genres


if __name__ == "__main__":
    app.run(debug=True, port=5000)