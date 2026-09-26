

"""Orders!C14 · ORD-011: POST /orders with a valid order must return HTTP 201 Created.

Written by Rowgate. The file name cites the cell; the test asserts the signed contract,
not the current behaviour of the code.
"""

# Fixtures come from tests/conftest.py:
#   client -> fastapi.testclient.TestClient on a fresh store

VALID_ORDER = {"sku": "KORA-TEE", "quantity": 2, "customer_id": "cus_001"}


def test_orders_C14_create_returns_201(client):
    """Orders!C14 · ORD-011: POST /orders valid order → 201 Created.

    Contract note (Orders!I14): POS treats any other 2xx as a failed checkout
    and retries (see INC-2291).
    """
    r = client.post("/orders", json=VALID_ORDER)
    assert r.status_code == 201

