import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_missing_payload():
    response = client.post("/analyze", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "Provide an image_url or ingredient list."


def test_analyze_with_ingredients(monkeypatch):
    def mock_analyze_text(_ingredients):
        return {"labels": ["Chicken", "Rice", "Spinach"]}

    monkeypatch.setattr("backend.routes.analysis.analyze_text", mock_analyze_text)

    payload = {
        "ingredients": ["chicken", "rice"],
        "goal": "fitness",
        "budget_min": 5,
        "budget_max": 12,
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] in {"Good", "Mid", "Bad"}
    assert "analysis_id" in data
    assert len(data["detected_items"]) > 0
