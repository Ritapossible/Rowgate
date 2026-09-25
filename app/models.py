"""Request and response models for the Kora partner API."""

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    sku: str = Field(min_length=1)
    quantity: int = Field(gt=0, le=100)
    customer_id: str = Field(min_length=1)


class OrderResponse(BaseModel):
    order_id: str
    # Internal name follows our req_* convention; the wire name stays request_id.
    req_id: str = Field(serialization_alias="request_id")
    status: str
    total_cents: int
    currency: str
    created_at: str


class InvoiceResponse(BaseModel):
    invoice_id: str
    order_id: str
    amount_cents: int
    tax_cents: int | None = None
    status: str
    issued_at: str
    due_date: str


class TokenRequest(BaseModel):
    grant_type: str
    client_id: str = Field(min_length=1)
    client_secret: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class ErrorBody(BaseModel):
    error: str
    error_description: str
