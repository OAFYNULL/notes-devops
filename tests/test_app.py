from app import app, notes


def reset_state():
    """Очистка хранилища заметок перед каждым тестом."""
    notes.clear()


def test_home_page():
    """Главная страница должна быть доступна и содержать заголовок."""
    reset_state()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "Notes" in response.text


def test_add_note():
    """Добавленная заметка должна появляться на главной странице."""
    reset_state()
    client = app.test_client()
    response = client.post("/add", data={"note": "Тестовая заметка"}, follow_redirects=True)
    assert response.status_code == 200
    assert "Тестовая заметка" in response.text
    assert len(notes) == 1


def test_delete_note():
    """После удаления заметка не должна отображаться в списке."""
    reset_state()
    client = app.test_client()
    client.post("/add", data={"note": "Заметка для удаления"}, follow_redirects=True)
    note_id = notes[0]["id"]
    response = client.get(f"/delete/{note_id}", follow_redirects=True)
    assert response.status_code == 200
    assert "Заметка для удаления" not in response.text
    assert len(notes) == 0


def test_empty_input_ignored():
    """Пустая заметка не должна добавляться в список."""
    reset_state()
    client = app.test_client()
    client.post("/add", data={"note": "   "}, follow_redirects=True)
    assert len(notes) == 0


def test_health_check():
    """Endpoint /health должен возвращать статус ok."""
    reset_state()
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_metrics_endpoint():
    """Endpoint /metrics должен отдавать данные в формате Prometheus."""
    reset_state()
    client = app.test_client()
    client.post("/add", data={"note": "Заметка для метрик"}, follow_redirects=True)
    response = client.get("/metrics")
    assert response.status_code == 200

    def metric_value(name):
        """Значение метрики из ответа Prometheus."""
        for line in response.text.splitlines():
            if line.startswith(name + " "):
                return float(line.split()[1])
        return None

    assert metric_value("notes_current") == 1.0
    assert metric_value("notes_created_total") >= 1.0
