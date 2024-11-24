from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.categories.models import CategoryOrm
from src.categories.schemas import CategoryAdd, ListCategoryAdd

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/add")
async def add_category(category_to_add: CategoryAdd, session: AsyncSession = Depends(get_async_session)):
    session.add(CategoryOrm(**category_to_add.model_dump()))
    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Category was added"})


@router.post("/add/many")
async def add_many_categories(categories_to_add: ListCategoryAdd, session: AsyncSession = Depends(get_async_session)):
    for category in categories_to_add.categories:
        session.add(CategoryOrm(**category.model_dump()))
    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Categories were added"})


@router.get("/category")
async def get_category(session: AsyncSession = Depends(get_async_session)):
    query = (select(CategoryOrm).options(selectinload(CategoryOrm.types)))

    categories = await session.execute(query)
    categories = categories.scalars().all()
    for category in categories:
        for tip in category.types:
            print(f"{category.title}: {tip.title}")

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ok"})
