import httpx
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.config import settings
from src.invoice.schemas import InvoiceData, InvoiceCreate

router = APIRouter(
    prefix="/invoice",
    tags=["Invoice"]
)


@router.post("/")
async def create_invoice_link(data: InvoiceData):
    invoice = InvoiceCreate()
    for item in data.items:
        label = f"{item['item']['title']} {item['size']['size']} x {item['quantity']}"
        amount = item['quantity'] * item['size']['price']

        invoice.prices.append({'label': label, 'amount': amount * 100})

    print(invoice)

    async with httpx.AsyncClient() as session:
        req = await session.post(settings.create_invoice_url, json=invoice.model_dump())

    if req.status_code == 200:
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"message": "Ok", "invoice_link": req.json()['result']})
