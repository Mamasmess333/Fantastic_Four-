import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_missing_image_url():
    # Case 1: No image_url in request
    response = client.post("/analyze", json={})
    assert response.status_code == 200
    assert response.json() == {"error": "Missing image_url"}


def test_valid_image_url(monkeypatch):
    # ✅ Mock the version imported inside routes.analysis
    def mock_analyze_image(url):
        return {"rating": "Good", "message": "Healthy meal!"}

    # Apply the mock directly to the route module used by FastAPI
    monkeypatch.setattr("routes.analysis.analyze_image", mock_analyze_image)

    # Case 2: Valid image_url input
    response = client.post("/analyze", json={"image_url": "https://example.com/food.jpg"})
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == "Good"
    assert "message" in data
