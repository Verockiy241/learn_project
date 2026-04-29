from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)

# Секретный ключ нужен для шифрования сессии, где хранятся flash-сообщения
app.secret_key = "super_secret_music_key_ISP239"
API_URL = "http://127.0.0.1:8000"


def get_int_or_none(val):
    return int(val) if val and val.strip() else None


def fetch_genres():
    """Получение списка жанров из API + жестко заданные шаблоны"""
    # Твои заготовленные шаблоны, которые будут в списке ВСЕГДА
    default_genres = ["Pluggnb", "Archivecore", "Ambient", "Glitch Hop", "Phonk", "Lo-Fi"]

    try:
        response = requests.get(f"{API_URL}/genres", timeout=5)
        db_genres = response.json() if response.ok else []

        # Складываем шаблоны и жанры из БД в один список
        # Используем set() чтобы убрать дубликаты (если шаблон уже есть в БД)
        all_genres = list(set(default_genres + db_genres))

        # Возвращаем отсортированный по алфавиту список
        return sorted(all_genres)
    except Exception:
        return sorted(default_genres)


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
        flash("Новый трек успешно добавлен!", "success")
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
        flash("Изменения сохранены!", "success")
        return redirect(url_for("track_list"))

    response = requests.get(f"{API_URL}/tracks/{track_id}", timeout=5)
    return render_template("form.html", track=response.json() if response.ok else None, genres=fetch_genres())


@app.route("/tracks/<int:track_id>/delete", methods=["POST"])
def delete_track(track_id: int):
    requests.delete(f"{API_URL}/tracks/{track_id}", timeout=5)
    flash("Трек удален!", "success")
    return redirect(url_for("track_list"))


@app.route("/tracks/bulk_delete", methods=["POST"])
def bulk_delete_tracks():
    track_ids = request.form.getlist("track_ids")
    if track_ids:
        ids_to_delete = [int(tid) for tid in track_ids]
        requests.post(f"{API_URL}/tracks/bulk-delete", json={"track_ids": ids_to_delete}, timeout=5)
        flash(f"Удалено треков: {len(ids_to_delete)}", "success")
    else:
        flash("Ничего не выбрано для удаления.", "warning")
    return redirect(url_for("track_list"))



if __name__ == "__main__":
    app.run(debug=True, port=5000)