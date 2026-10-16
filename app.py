import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Простое хранилище заметок в памяти (для учебного проекта).
# Каждая заметка — словарь {id, text, created}.
notes = []
next_id = 1

# Пользовательские метрики Prometheus
notes_created = Counter("notes_created", "Total number of created notes")
notes_deleted = Counter("notes_deleted", "Total number of deleted notes")
notes_current = Gauge("notes_current", "Current number of notes in the list")


@app.route("/")
def index():
    """Главная страница со списком заметок."""
    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
def add_note():
    """Добавление новой заметки через HTML-форму."""
    global next_id
    text = request.form.get("note", "").strip()
    if text:
        notes.append(
            {
                "id": next_id,
                "text": text,
                "created": datetime.now().strftime("%d.%m.%Y %H:%M"),
            }
        )
        next_id += 1
        notes_created.inc()
        notes_current.set(len(notes))
    return redirect(url_for("index"))


@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    """Удаление заметки по идентификатору."""
    global notes
    before = len(notes)
    notes[:] = [n for n in notes if n["id"] != note_id]
    if len(notes) < before:
        notes_deleted.inc()
        notes_current.set(len(notes))
    return redirect(url_for("index"))


@app.route("/health")
def health():
    """Проверка работоспособности приложения."""
    return {"status": "ok"}


@app.route("/metrics")
def metrics():
    """Endpoint метрик в формате Prometheus."""
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
