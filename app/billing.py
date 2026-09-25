from datetime import datetime, timedelta, timezone

from fastapi import APIRouter

from app import store
from app.errors import error_response
from app.models import InvoiceResponse

router = APIRouter()


def create_invoice_for(order) -> InvoiceResponse:
    issued = datetime.now(timezone.utc)
    invoice = InvoiceResponse(
        invoice_id=order.order_id.replace("ord_", "inv_"),
        order_id=order.order_id,
        amount_cents=order.total_cents,
        tax_cents=round(order.total_cents * store.TAX_RATE),
        currency=order.currency,
        status="open",
        issued_at=issued.isoformat(timespec="seconds"),
        due_date=(issued + timedelta(days=30)).date().isoformat(),
    )
    store.INVOICES[invoice.invoice_id] = invoice.model_dump()
    return invoice


@router.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: str):
    invoice = store.INVOICES.get(invoice_id)
    if invoice is None:
        return error_response(404, "not_found", f"invoice {invoice_id} does not exist")
    return InvoiceResponse(**invoice)
