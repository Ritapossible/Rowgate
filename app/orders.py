import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Header, status

from app import store
from app.errors import error_response
from app.models import OrderCreate, OrderResponse
from app.billing import create_invoice_for

router = APIRouter()
log = logging.getLogger("kora.orders")


def _price_cents(sku: str, quantity: int) -> int:
    return store.PRICES_CENTS.get(sku, store.DEFAULT_PRICE_CENTS) * quantity


# Fast checkout: accept the order immediately and confirm it asynchronously,
# so the POS no longer waits on invoice creation.
@router.post("/orders", status_code=status.HTTP_202_ACCEPTED, response_model=OrderResponse)
def create_order(body: OrderCreate, x_request_id: str | None = Header(default=None)) -> OrderResponse:
    order_id = f"ord_{uuid.uuid4().hex[:12]}"
    order = OrderResponse(
        order_id=order_id,
        req_id=x_request_id or f"req_{uuid.uuid4().hex[:12]}",
        status="pending",
        total_cents=_price_cents(body.sku, body.quantity),
        currency=store.CURRENCY,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    store.ORDERS[order_id] = order.model_dump()
    create_invoice_for(order)
    log.info("order accepted %s sku=%s qty=%d", order_id, body.sku, body.quantity)
    return order


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    order = store.ORDERS.get(order_id)
    if order is None:
        return error_response(404, "not_found", f"order {order_id} does not exist")
    return OrderResponse(**order)
