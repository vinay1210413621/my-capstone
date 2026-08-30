import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness_check():
    """Test readiness check endpoint"""
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_create_item():
    """Test create item endpoint"""
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 19.99
    }
    response = client.post("/items", json=item_data)
    assert response.status_code == 200
    assert response.json()["item"]["name"] == "Test Item"


def test_get_item():
    """Test get item endpoint"""
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["item_id"] == 1
