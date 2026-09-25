import secrets

from fastapi import APIRouter

from app.errors import error_response
from app.models import TokenRequest, TokenResponse

router = APIRouter()

# Demo credentials only. A real service reads these from a secret store.
CLIENTS = {"kora-pos": "demo-secret-kora-pos"}
SUPPORTED_GRANTS = {"client_credentials"}


@router.post("/auth/token", response_model=TokenResponse)
def issue_token(body: TokenRequest):
    if body.grant_type not in SUPPORTED_GRANTS:
        return error_response(400, "unsupported_grant_type", f"grant_type {body.grant_type} is not supported")
    if CLIENTS.get(body.client_id) != body.client_secret:
        return error_response(401, "invalid_grant", "Client authentication failed")
    return TokenResponse(access_token=secrets.token_urlsafe(24), token_type="Bearer", expires_in=3600)
