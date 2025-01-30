from random import choices
from string import ascii_uppercase, digits

from pydantic import BaseModel

from src.config import settings


class InvoiceCreate(BaseModel):
    title: str = 'Заказ'
    description: str = 'Оплата заказа из ресторана вкусно'
    provider_token: str = settings.PROVIDER_TOKEN
    currency: str = "RUB"
    payload: str = ''.join(choices(ascii_uppercase + digits, k=10))
    prices: list = []


class InvoiceData(BaseModel):
    chat_id: int
    items: list
    total_price: int
