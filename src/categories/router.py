import json

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.categories.models import CategoryOrm
from src.categories.schemas import CategoryAdd, CategoryDTO, CategoryDelete, CategoriesWithItemsDTO
from src.database import get_async_session
from src.items.models import ItemOrm
from src.service import redis_class as redis
from src.types.models import TypeOrm

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/")
async def get_all_categories(session: AsyncSession = Depends(get_async_session)):
    categories = await session.execute(select(CategoryOrm))
    categories = categories.scalars().all()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": [
                                                                     CategoryDTO.from_orm_to_json(category)
                                                                     for category in categories
                                                                 ]})


@router.get('/load_items_to_json')
async def load_to_json(session: AsyncSession = Depends(get_async_session)):
    categories = await session.scalars((select(CategoryOrm)
                                        .options(selectinload(CategoryOrm.types)
                                                 .selectinload(TypeOrm.items)
                                                 .selectinload(ItemOrm.sizes))))
    categories = categories.all()
    categories = [(CategoriesWithItemsDTO.from_orm_to_json(category))
                  for category in categories
                  ]

    with open('menu.json', 'w', encoding='UTF-8') as file:
        json.dump(categories, file, ensure_ascii=False)


@router.get("/by_id/{category_id}")
async def get_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    category = await session.get(CategoryOrm, category_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                 "data": CategoryDTO.from_orm_to_json(category)})


@router.get("/items")
async def get_items_from_categories(session: AsyncSession = Depends(get_async_session)):
    cache = redis.get('items')

    if cache:
        print('cached')
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                     "data": json.loads(cache)})

    else:
        categories = await session.scalars((select(CategoryOrm)
                                            .options(selectinload(CategoryOrm.types)
                                                     .selectinload(TypeOrm.items)
                                                     .selectinload(ItemOrm.sizes))))
        categories = categories.all()
        categories = [(CategoriesWithItemsDTO.from_orm_to_json(category))
                      for category in categories
                      ]
        redis.set('items', json.dumps(categories))
        print('not cached')
        redis.expire('items', 5)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok",
                                                                     "data": categories})


@router.post("/add")
async def add_category(category_to_add: CategoryAdd, session: AsyncSession = Depends(get_async_session)):
    category = CategoryOrm(**category_to_add.model_dump())
    session.add(category)
    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Category was added"})


@router.post("/many")
async def add_many_categories(categories_to_add: list[CategoryAdd], session: AsyncSession = Depends(get_async_session)):
    categories = [CategoryOrm(**category.model_dump()) for category in categories_to_add]
    session.add_all(categories)
    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Categories were added"})


@router.delete("/")
async def delete_category(category: CategoryDelete, session: AsyncSession = Depends(get_async_session)):
    category_to_delete = await session.get(CategoryOrm, category.id)

    await session.delete(category_to_delete)

    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Category was deleted"})


@router.delete("/many")
async def delete_many_categories(categories: list[CategoryDelete], session: AsyncSession = Depends(get_async_session)):
    categories_to_delete = [await session.get(CategoryOrm, category.id) for category in categories]

    [await session.delete(category_to_delete) for category_to_delete in categories_to_delete]

    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Categories were deleted"})
