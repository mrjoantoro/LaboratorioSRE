# src/tests/test_main.py
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_product():
    response = client.post("/api/products", json={
        "name": "Laptop",
        "description": "Laptop perdida en el parque",
        "location": "Parque Central",
        "date_lost": "2024-08-08"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Product registered successfully"

def test_read_products():
    response = client.get("/api/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
