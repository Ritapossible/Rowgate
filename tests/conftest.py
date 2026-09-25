import pytest
from fastapi.testclient import TestClient

from app import store
from app.main import app


@pytest.fixture
def client():
    store.reset()
    return TestClient(app)


@pytest.fixture
def order(client):
    r = client.post(
        "/orders",
        json={"sku": "KORA-TEE", "quantity": 2, "customer_id": "cus_001"},
        headers={"X-Request-ID": "req_test_001"},
    )
    return r.json()
