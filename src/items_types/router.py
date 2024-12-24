from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.items_types.models import ItemTypeOrm
from src.items_types.schemas import ItemTypeAdd, ItemTypeDTO, ItemTypesDelete, ItemTypeDelete

router = APIRouter(
    prefix="/items_types",
    tags=["Items Types"]
)


@router.get("/")
async def get_all_items_types(session: AsyncSession = Depends(get_async_session)):
    items_types = await session.execute(select(ItemTypeOrm))
    items_types = items_types.scalars().all()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": [
                                                                     ItemTypeDTO.from_orm_to_json(item_type)
                                                                     for item_type in items_types
                                                                 ]})


@router.get("/{item_id}")
async def get_item_types(item_id: int, session: AsyncSession = Depends(get_async_session)):
    item_types = await session.execute(select(ItemTypeOrm).filter_by(item_id=item_id))
    item_types = item_types.scalars().all()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": [
                                                                     ItemTypeDTO.from_orm_to_json(item_type)
                                                                     for item_type in item_types
                                                                 ]})


@router.post("/")
async def add_item_to_type(item_type_add: ItemTypeAdd, session: AsyncSession = Depends(get_async_session)):
    item_type = ItemTypeOrm(**item_type_add.model_dump())
    session.add(item_type)

    await session.commit()
    await session.refresh(item_type)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Item was added to type",
                                                                      "data": ItemTypeDTO.from_orm_to_json(item_type)})


@router.post("/many")
async def add_many_items_to_many_types(items_types_add: list[ItemTypeAdd],
                                       session: AsyncSession = Depends(get_async_session)):
    items_types = [ItemTypeOrm(**item_type.model_dump()) for item_type in items_types_add]
    session.add_all(items_types)

    await session.commit()
    [await session.refresh(item_type) for item_type in items_types]

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Items were added to types",
                                                                      "data": [
                                                                          ItemTypeDTO.from_orm_to_json(item_type)
                                                                          for item_type in items_types
                                                                      ]})


@router.delete("/")
async def delete_item_from_type(item: ItemTypeDelete, session: AsyncSession = Depends(get_async_session)):
    item_type = await session.get(ItemTypeOrm, (item.item_id, item.type_id))

    await session.delete(item_type)

    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Item was deleted from type"})


@router.delete("/many_types")
async def delete_item_from_all_types(item: ItemTypesDelete, session: AsyncSession = Depends(get_async_session)):
    item_types = await session.execute(select(ItemTypeOrm).filter_by(item_id=item.item_id))
    item_types = item_types.scalars().all()

    [await session.delete(item_type) for item_type in item_types]

    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Item was deleted from all types"})


@router.delete("/many_items")
async def delete_many_items_from_all_types(items: list[ItemTypesDelete],
                                           session: AsyncSession = Depends(get_async_session)):
    items_types = [await session.execute(select(ItemTypeOrm).filter_by(item_id=item.item_id)) for item in items]
    items_types = [item_types.scalars().all() for item_types in items_types]

    [[await session.delete(item_type) for item_type in item_types] for item_types in items_types]

    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Items were deleted from all types"})
