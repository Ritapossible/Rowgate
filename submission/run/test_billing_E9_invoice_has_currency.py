"""Billing!E9 · BIL-007: GET /invoices/{id} response must include field `currency` (string, ISO 4217, Required=Y).

Written by Rowgate. The file name cites the cell; the test asserts the signed contract,
not the current behaviour of the code.
"""

# Fixtures come from tests/conftest.py:
#   client -> fastapi.testclient.TestClient on a fresh store
#   order  -> JSON of an order created with X-Request-ID: req_test_001

VALID_ORDER = {"sku": "KORA-TEE", "quantity": 2, "customer_id": "cus_001"}


def test_billing_E9_invoice_has_currency(client):
    """Billing!E9 · BIL-007: GET /invoices/{id} must return `currency` field.

    Contract note (Billing!I9): Mandatory for multi-currency settlement.
    Partner ledger rejects invoices without it.
    """
    r_order = client.post("/orders", json=VALID_ORDER)
    order_id = r_order.json()["order_id"]
    invoice_id = order_id.replace("ord_", "inv_")

    r = client.get(f"/invoices/{invoice_id}")
    assert r.status_code == 200
    assert "currency" in r.json(), "currency field is required (BIL-007)"
