from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.database import get_async_session
from src.items.models import ItemOrm, ItemTypeOrm
from src.items.schemas import ItemAdd, ListItemAdd, ItemTypeAdd, ListItemTypeAdd
from src.types.models import TypeOrm

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.post("/add")
async def add_item(new_item: ItemAdd, session: AsyncSession = Depends(get_async_session)):
    session.add(ItemOrm(**new_item.model_dump()))

    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Item was added"})


@router.post("/add/many")
async def add_items(new_items: ListItemAdd, session: AsyncSession = Depends(get_async_session)):
    session.add_all([ItemOrm(**item.model_dump()) for item in new_items.items])

    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Items were added"})


@router.delete("/delete")
async def delete_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    item = await session.get(ItemOrm, item_id)

    await session.delete(item)

    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Item was deleted"})


@router.delete("/delete/many")
async def delete_items(item_ids: list[int], session: AsyncSession = Depends(get_async_session)):
    items = [await session.get(ItemOrm, item_id) for item_id in item_ids]

    for item in items:
        await session.delete(item)

    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Items were deleted"})


@router.post("/add/type")
async def add_item_to_type(item: ItemTypeAdd, session: AsyncSession = Depends(get_async_session)):
    session.add(ItemTypeOrm(**item.model_dump()))

    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Item was added to type"})


@router.post("/add/types")
async def add_items_to_types(items: ListItemTypeAdd, session: AsyncSession = Depends(get_async_session)):
    session.add_all([ItemTypeOrm(**item.model_dump()) for item in items.items])

    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Items were added to types"})


@router.get("/all")
async def get_all_items(session: AsyncSession = Depends(get_async_session)):
    query = (select(ItemOrm)
             .options(selectinload(ItemOrm.types).joinedload(TypeOrm.category)))

    items = await session.execute(query)
    items = items.scalars().all()

    for item in items:
        print('')
        print(item, end=', ')
        for tip in item.types:
            print(tip.title, tip.category.title, end=', ')

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok"})
