from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.types.models import *
from src.types.schemas import AddTypesToItems
from src.types.utils import validate_categories_of_items

router = APIRouter(
    prefix="/types",
    tags=["Types"]
)


@router.post("/add/many")
async def add_types_to_items(items_to_add: AddTypesToItems, session: AsyncSession = Depends(get_async_session)):
    await validate_categories_of_items(items_to_add)

    print('ok')

    return
