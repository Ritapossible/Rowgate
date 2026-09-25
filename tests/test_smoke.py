"""Smoke tests: the service starts and each endpoint answers."""


def test_health(client):
    assert client.get("/health").json() == {"ok": True}


def test_create_order_succeeds(client):
    r = client.post("/orders", json={"sku": "KORA-MUG", "quantity": 1, "customer_id": "cus_002"})
    assert r.is_success
    assert r.json()["order_id"].startswith("ord_")


def test_order_total(client):
    r = client.post("/orders", json={"sku": "KORA-TEE", "quantity": 3, "customer_id": "cus_003"})
    assert r.json()["total_cents"] == 7500


def test_get_order(client, order):
    r = client.get(f"/orders/{order['order_id']}")
    assert r.status_code == 200
    assert r.json()["order_id"] == order["order_id"]


def test_unknown_order(client):
    assert client.get("/orders/ord_missing").status_code == 404


def test_invoice_created_with_order(client, order):
    invoice_id = order["order_id"].replace("ord_", "inv_")
    r = client.get(f"/invoices/{invoice_id}")
    assert r.status_code == 200
    assert r.json()["amount_cents"] == order["total_cents"]


def test_token_issued(client):
    r = client.post(
        "/auth/token",
        json={"grant_type": "client_credentials", "client_id": "kora-pos", "client_secret": "demo-secret-kora-pos"},
    )
    assert r.status_code == 200
    assert r.json()["token_type"] == "Bearer"


def test_token_rejects_bad_secret(client):
    r = client.post(
        "/auth/token",
        json={"grant_type": "client_credentials", "client_id": "kora-pos", "client_secret": "wrong"},
    )
    assert r.status_code >= 400
