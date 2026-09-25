import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Header, status

from app import store
from app.errors import error_response
from app.models import OrderCreate, OrderResponse
from app.billing import create_invoice_for

router = APIRouter()


@router.post("/orders", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def create_order(body: OrderCreate, x_request_id: str | None = Header(default=None)) -> OrderResponse:
    order_id = f"ord_{uuid.uuid4().hex[:12]}"
    unit_price = store.PRICES_CENTS.get(body.sku, store.DEFAULT_PRICE_CENTS)
    order = OrderResponse(
        order_id=order_id,
        request_id=x_request_id or f"req_{uuid.uuid4().hex[:12]}",
        status="confirmed",
        total_cents=unit_price * body.quantity,
        currency=store.CURRENCY,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    store.ORDERS[order_id] = order.model_dump()
    create_invoice_for(order)
    return order


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    order = store.ORDERS.get(order_id)
    if order is None:
        return error_response(404, "not_found", f"order {order_id} does not exist")
    return OrderResponse(**order)
