"""Smoke tests for the Flask routes. No LLM / network required."""

import app


def _client():
    return app.app.test_client()


def test_health_ok():
    resp = _client().get("/api/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert "default_ollama_model" in data


def test_index_renders():
    resp = _client().get("/")
    assert resp.status_code == 200
    assert b"Math" in resp.data


def test_generate_requires_a_prompt():
    resp = _client().post("/api/generate", json={})
    assert resp.status_code == 400


def test_neuro_symbolic_requires_a_prompt():
    resp = _client().post("/api/neuro_symbolic", json={})
    assert resp.status_code == 400
