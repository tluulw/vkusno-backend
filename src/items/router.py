from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.items.models import ItemOrm
from src.items.schemas import ItemDTO, ItemDelete, ItemWithSizeAdd
from src.items.service import _get_items, _add_items, _get_all_items, _get_item

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.get("/")
async def get_all_items(session: AsyncSession = Depends(get_async_session)):
    # Получаем все items
    items = await _get_all_items(session)

    # Возвращаем ответ со списком всех items
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": [
                                                                     ItemDTO.from_orm_to_json(item)
                                                                     for item in items
                                                                 ]})


@router.get("/{item_id}")
async def get_item_with_sizes(item_id: int, session: AsyncSession = Depends(get_async_session)):
    # Получаем item по id
    item = await _get_item(session, item_id)

    # Возвращаем ответ с одним item'ом
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": ItemDTO.from_orm_to_json(item)
                                                                 })


@router.post("/")
async def add_item(new_item: ItemWithSizeAdd, session: AsyncSession = Depends(get_async_session)):
    # Добавляем новую позицию и размеры в сессию и получаем id позиции
    item_ids = await _add_items(session, [new_item])

    # Получаем наш item по id
    item = await _get_item(session, item_ids[0])

    await session.commit()

    # Выводим добавленный item
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Item was added",
                                                                      "data": ItemDTO.from_orm_to_json(item)
                                                                      })


@router.post("/many")
async def add_many_items(new_items: list[ItemWithSizeAdd], session: AsyncSession = Depends(get_async_session)):
    # Добавляем новые позиции и их размеры в сессию и получаем id добавленных позиций в списке
    item_ids = await _add_items(session, new_items)

    # Получаем наши item'ы по id
    items = await _get_items(session, item_ids)

    await session.commit()

    # Выводим добавленные item'ы
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Items were added",
                                                                      "data": [
                                                                          ItemDTO.from_orm_to_json(item)
                                                                          for item in items
                                                                      ]
                                                                      })


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
