from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.types.models import TypeOrm
from src.types.schemas import TypeAdd, TypeDTO, TypeDelete

router = APIRouter(
    prefix="/types",
    tags=["Types"]
)


@router.get("/")
async def get_all_types(session: AsyncSession = Depends(get_async_session)):
    types = await session.execute(select(TypeOrm))
    types = types.scalars().all()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": [
                                                                     TypeDTO.from_orm_to_json(tip)
                                                                     for tip in types
                                                                 ]})


@router.get("/{type_id}")
async def get_type(type_id: int, session: AsyncSession = Depends(get_async_session)):
    tip = await session.get(TypeOrm, type_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": TypeDTO.from_orm_to_json(tip)})


@router.post("/")
async def add_type(type_to_add: TypeAdd, session: AsyncSession = Depends(get_async_session)):
    tip = TypeOrm(**type_to_add.model_dump())
    session.add(tip)
    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Type was added"})


@router.post("/many")
async def add_many_types(types_to_add: list[TypeAdd], session: AsyncSession = Depends(get_async_session)):
    types = [TypeOrm(**tip.model_dump()) for tip in types_to_add]
    session.add_all(types)
    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Types were added"})


@router.delete("/")
async def delete_type(tip: TypeDelete, session: AsyncSession = Depends(get_async_session)):
    type_to_delete = await session.get(TypeOrm, tip.id)

    await session.delete(type_to_delete)

    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Type was deleted"})


@router.delete("/many")
async def delete_many_types(types: list[TypeDelete], session: AsyncSession = Depends(get_async_session)):
    types_to_delete = [await session.get(TypeOrm, tip.id) for tip in types]

    [await session.delete(type_to_delete) for type_to_delete in types_to_delete]

    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Types were deleted"})
