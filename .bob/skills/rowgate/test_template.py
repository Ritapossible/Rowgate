"""<Sheet>!<Cell> · <RULE-ID>: <what the contract row says, in one line>.

Written by Rowgate. The file name cites the cell; the test asserts the signed contract,
not the current behaviour of the code.
"""

# Fixtures come from tests/conftest.py:
#   client -> fastapi.testclient.TestClient on a fresh store
#   order  -> JSON of an order created with X-Request-ID: req_test_001

VALID_ORDER = {"sku": "KORA-TEE", "quantity": 2, "customer_id": "cus_001"}
VALID_CLIENT = {"grant_type": "client_credentials", "client_id": "kora-pos", "client_secret": "demo-secret-kora-pos"}


def test_sheet_A1_what(client):  # rename: test_<sheet>_<cell>_<what>
    r = client.post("/orders", json=VALID_ORDER)          # or client.get(...)
    assert r.status_code == 201                            # value from the cited cell
    # for a required field:  assert "currency" in r.json()
    # for an error envelope: assert r.json() == {"error": "...", "error_description": "..."}
