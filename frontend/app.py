from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:8000"

def get_int_or_none(val):
    return int(val) if val and val.strip() else None

@app.route("/")
def index():
    # Главная страница (index.html)
    return render_template("index.html")

@app.route("/tracks")
def track_list():
    # Страница со списком треков (list.html)
    try:
        response = requests.get(f"{API_URL}/tracks", timeout=5)
        tracks = response.json() if response.ok else []
    except Exception:
        tracks = []
    return render_template("list.html", tracks=tracks)

@app.route("/tracks/create", methods=["GET", "POST"])
def create_track():
    # Форма добавления (form.html)
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
    return render_template("form.html", track=None)

@app.route("/tracks/<int:track_id>/edit", methods=["GET", "POST"])
def edit_track(track_id: int):
    # Форма редактирования (form.html)
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
    return render_template("form.html", track=response.json() if response.ok else None)

@app.route("/tracks/<int:track_id>/delete", methods=["POST"])
def delete_track(track_id: int):
    requests.delete(f"{API_URL}/tracks/{track_id}", timeout=5)
    return redirect(url_for("track_list"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)