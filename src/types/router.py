from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.types.models import TypeOrm
from src.types.schemas import TypeAdd, ListTypeAdd

router = APIRouter(
    prefix="/types",
    tags=["Types"]
)


@router.post("/add")
async def add_types_to_items(type_to_add: TypeAdd, session: AsyncSession = Depends(get_async_session)):
    session.add(TypeOrm(**type_to_add.model_dump()))
    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Type was added"})


@router.post("/add/many")
async def add_many_types(types_to_add: ListTypeAdd, session: AsyncSession = Depends(get_async_session)):
    session.add_all([TypeOrm(**tip.model_dump()) for tip in types_to_add.types])
    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Types were added"})