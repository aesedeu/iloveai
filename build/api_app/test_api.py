from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Api_Name": "Get slices"}


def test_available_images():
    response = client.get("/api/available_images")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_slice():
    data = {
        "image_name": "example_image",
        "min_depth": 0.0,
        "max_depth": 10.0
    }
    response = client.post("/api/get_slice", json=data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
