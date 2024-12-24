from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.items.models import ItemOrm
from src.items.schemas import ItemAdd, ItemDTO, ItemDelete

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.get("/")
async def get_all_items(session: AsyncSession = Depends(get_async_session)):
    items = await session.execute(select(ItemOrm))
    items = items.scalars().all()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": [
                                                                     ItemDTO.from_orm_to_json(item)
                                                                     for item in items
                                                                 ]})


@router.get("/{item_id}")
async def get_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    item = await session.get(ItemOrm, item_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": [
                                                                     ItemDTO.from_orm_to_json(item)
                                                                 ]})


@router.post("/")
async def add_item(new_item: ItemAdd, session: AsyncSession = Depends(get_async_session)):
    item = ItemOrm(**new_item.model_dump())
    session.add(item)

    await session.commit()
    await session.refresh(item)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Item was added",
                                                                      "data":
                                                                          ItemDTO.from_orm_to_json(item)
                                                                      })


@router.post("/many")
async def add_many_items(new_items: list[ItemAdd], session: AsyncSession = Depends(get_async_session)):
    items = [ItemOrm(**new_item.model_dump()) for new_item in new_items]
    session.add_all(items)

    await session.commit()
    [await session.refresh(item) for item in items]

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Items were added",
                                                                      "data": [
                                                                          ItemDTO.from_orm_to_json(item)
                                                                          for item in items
                                                                      ]})


@router.delete("/")
async def delete_item(item: ItemDelete, session: AsyncSession = Depends(get_async_session)):
    item = await session.get(ItemOrm, item.id)

    await session.delete(item)

    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Item was deleted"})


@router.delete("/many")
async def delete_many_items(items: list[ItemDelete], session: AsyncSession = Depends(get_async_session)):
    items_to_delete = [await session.get(ItemOrm, item.id) for item in items]

    [await session.delete(item) for item in items_to_delete]

    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Items were deleted"})
