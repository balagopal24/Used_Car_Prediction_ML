"""
tests/test_api.py
Basic sanity tests for the FastAPI endpoints.
Run with: pytest tests/
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_predict_valid_payload():
    payload = {
        "brand": "Maruti",
        "fuel": "Petrol",
        "transmission": "Manual",
        "owner": "First Owner",
        "year": 2018,
        "km_driven": 40000,
        "engine_cc": 1200,
        "mileage_kmpl": 18.0,
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    assert "predicted_price" in resp.json()
    assert resp.json()["predicted_price"] > 0
