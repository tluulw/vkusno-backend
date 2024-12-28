from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.items_sizes.models import ItemSizeOrm
from src.items_sizes.schemas import ItemSizeAdd, ItemSizeDTO, ItemSizeDelete
from src.items_sizes.service import _add_sizes

router = APIRouter(
    prefix="/items_sizes",
    tags=["Items Sizes"]
)


@router.get("/")
async def get_all_items_sizes(session: AsyncSession = Depends(get_async_session)):
    items_sizes = await session.execute(select(ItemSizeOrm).order_by(ItemSizeOrm.item_id, ItemSizeOrm.price))
    items_sizes = items_sizes.scalars().all()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": [
                                                                     ItemSizeDTO.from_orm_to_json(item_size)
                                                                     for item_size in items_sizes
                                                                 ]})


@router.get("/{item_id}")
async def get_item_sizes(item_id: int, session: AsyncSession = Depends(get_async_session)):
    item_sizes = await session.execute(select(ItemSizeOrm)
                                       .filter_by(item_id=item_id)
                                       .order_by(ItemSizeOrm.item_id, ItemSizeOrm.price))
    item_sizes = item_sizes.scalars().all()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": [
                                                                     ItemSizeDTO.from_orm_to_json(item_size)
                                                                     for item_size in item_sizes
                                                                 ]})


@router.post("/")
async def add_size_to_item(size: ItemSizeAdd, session: AsyncSession = Depends(get_async_session)):
    await _add_sizes([size], session)

    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Size was added to item"})


@router.post("/many")
async def add_many_sizes_to_items(sizes: list[ItemSizeAdd], session: AsyncSession = Depends(get_async_session)):
    await _add_sizes(sizes, session)

    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Sizes were added to items"})


@router.delete("/")
async def delete_size_of_item(size: ItemSizeDelete, session: AsyncSession = Depends(get_async_session)):
    size_to_delete = await session.get(ItemSizeOrm, (size.item_id, size.size))

    await session.delete(size_to_delete)
    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Size of item was deleted"})


@router.delete("/many")
async def delete_many_sizes_of_items(sizes: list[ItemSizeDelete], session: AsyncSession = Depends(get_async_session)):
    sizes_to_delete = [await session.get(ItemSizeOrm, (size.item_id, size.size)) for size in sizes]

    [await session.delete(size) for size in sizes_to_delete]
    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Sizes of items were deleted"})
