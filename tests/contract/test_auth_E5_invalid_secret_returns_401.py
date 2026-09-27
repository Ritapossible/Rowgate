"""Auth!E5 · AUT-002: POST /auth/token with wrong client_secret must return HTTP 401.

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


def test_auth_E5_invalid_secret_returns_401(client):
    """Auth!E5 · AUT-002: wrong client_secret → HTTP 401.

    Contract note (Auth!H5): POS shows 're-enter API key' only on 401 + invalid_grant.
    """
    r = client.post("/auth/token", json=WRONG_SECRET)
    assert r.status_code == 401
