"""Auth!D5 · AUT-002 / ERR-004: wrong client_secret error body must use the shared error envelope.

Expected: {"error": "invalid_grant", "error_description": "Client authentication failed"}
FastAPI's default {"detail": ...} is NOT accepted by POS.

Written by Rowgate. The file name cites the cell; the test asserts the signed contract,
not the current behaviour of the code.
"""

# Fixtures come from tests/conftest.py:
#   client -> fastapi.testclient.TestClient on a fresh store

WRONG_SECRET = {
    "grant_type": "client_credentials",
    "client_id": "kora-pos",
    "client_secret": "wrong-secret",
}


def test_auth_D5_invalid_secret_error_envelope(client):
    """Auth!D5 · AUT-002 / ERR-004: wrong client_secret → error envelope with invalid_grant.

    Related cell: Errors!D6
    Contract: {"error": "invalid_grant", "error_description": "Client authentication failed"}
    error_description text is shown to cashiers verbatim (Errors!F6).
    """
    r = client.post("/auth/token", json=WRONG_SECRET)
    body = r.json()
    assert body == {
        "error": "invalid_grant",
        "error_description": "Client authentication failed",
    }
