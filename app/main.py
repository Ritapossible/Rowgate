"""Kora partner API: orders, billing and auth for the Kora POS integration."""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app import auth, billing, orders
from app.errors import validation_error_handler

app = FastAPI(title="Kora Partner API", version="3.2.0")
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.include_router(orders.router)
app.include_router(billing.router)
app.include_router(auth.router)


@app.get("/health")
def health() -> dict:
    return {"ok": True}
