# Service - Data Access Layer(DAL). Для бизнес логики, связанной с item
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.items.models import ItemOrm
from src.items.schemas import ItemAdd
from src.items_sizes.schemas import ItemSizeAdd
from src.items_sizes.service import _add_sizes


# Получить определённый item
async def _get_item(session, item_id: int):
    # Функция принимает сессию, id item'а, отдаёт нужный item
    item = await session.execute(
        select(ItemOrm)
        .filter_by(id=item_id)
        .options(selectinload(ItemOrm.sizes))
    )
    return item.scalars().first()


# Получить несколько определённых item'ов
async def _get_items(session, item_ids: list[int]):
    # Функция принимает сессию, id item'ов в списке, отдаёт список из item'ов с нужными id
    item = await session.execute(
        select(ItemOrm)
        .filter(ItemOrm.id.in_(item_ids))
        .options(selectinload(ItemOrm.sizes))
    )
    return item.scalars().all()


# Получить все items
async def _get_all_items(session):
    # Функция принимает сессию, отдаёт список из всех item'ов
    items = await session.execute(
        select(ItemOrm)
        .options(selectinload(ItemOrm.sizes))
    )
    return items.scalars().all()


# Добавляем item'ы в сессию
async def _add_items(session, items_to_add: list):
    # Формируем список из orm объектов item'ов
    items = [
        ItemOrm(
            **ItemAdd(  # формируем схемку для добавления item'а
                **item_to_add.model_dump()  # раскрываем изначальную схемку
            ).model_dump()  # раскрываем сформированную схемку
        )
        for item_to_add in items_to_add  # для каждого item'а
    ]

    # Добавляем item'ы в сессию
    session.add_all(items)
    # Делаем flush и refresh, чтобы мы могли обратиться к item.id
    await session.flush()
    [await session.refresh(item) for item in items]

    # Добавляем размеры item'ов в сессию
    for item in items:  # проход по item'ам для получения id
        for item_to_add in items_to_add:  # проход по полным item'ам для получения sizes
            if item.title == item_to_add.title:  # сравнение, что это один и тот же item
                await _add_sizes([
                    ItemSizeAdd(item_id=item.id, **size.model_dump())  # формиурем схемку для item_size
                    for size in item_to_add.sizes  # для каждого размера
                ], session)  # добавление item_size в сессию

    # возвращаем список id item'ов
    return [item.id for item in items]
