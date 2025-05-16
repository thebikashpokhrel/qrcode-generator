import pytest
from fastapi.testclient import TestClient

from app.main import app

TEST_USER_ID = "testuser"
TEST_CONTENT = "hello pytest"

def test_generate_qr():
    with TestClient(app) as client:
        response = client.post("/generate/", params={"content": TEST_CONTENT, "user_id": TEST_USER_ID})
        assert response.status_code == 200
        data = response.json()
        assert "download_url" in data
        assert data["download_url"].endswith(data["filename"])

def test_download_qr():
    with TestClient(app) as client:
        # First generate the QR code
        response = client.post("/generate/", params={"content": TEST_CONTENT, "user_id": TEST_USER_ID})
        assert response.status_code == 200
        filename = response.json()["filename"]
        
        # Then download it
        response = client.get(f"/download/{filename}")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

def test_history():
    with TestClient(app) as client:
        client.post("/generate/", params={"content": TEST_CONTENT, "user_id": TEST_USER_ID})
        response = client.get(f"/history/{TEST_USER_ID}")
        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert isinstance(data["history"], list)
        assert len(data["history"]) > 0
        for item in data["history"]:
            assert "download_url" in item
            assert "/download/" in item["download_url"]
