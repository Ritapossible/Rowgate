import secrets

from fastapi import APIRouter, HTTPException

from app.errors import error_response
from app.models import TokenRequest, TokenResponse

router = APIRouter()

# Demo credentials only. A real service reads these from a secret store.
CLIENTS = {"kora-pos": "demo-secret-kora-pos"}
SUPPORTED_GRANTS = {"client_credentials"}


def _is_valid_client(client_id: str, client_secret: str) -> bool:
    expected = CLIENTS.get(client_id)
    return expected is not None and secrets.compare_digest(expected, client_secret)


@router.post("/auth/token", response_model=TokenResponse)
def issue_token(body: TokenRequest):
    if body.grant_type not in SUPPORTED_GRANTS:
        return error_response(400, "unsupported_grant_type", f"grant_type {body.grant_type} is not supported")
    if not _is_valid_client(body.client_id, body.client_secret):
        raise HTTPException(status_code=400, detail="invalid client credentials")
    return TokenResponse(access_token=secrets.token_urlsafe(24), token_type="Bearer", expires_in=3600)
