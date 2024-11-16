import asyncio

from fastapi.exceptions import HTTPException

from src.constants import TYPES_FOR_CATEGORIES
from src.types.schemas import AddTypesToItems


async def validate_category_of_item(category, typ):
    await validate_category(category)
    await validate_type(category, typ)


async def validate_categories_of_item(categories_types: list[list]):
    await asyncio.gather(*[validate_category_of_item(*category_type) for category_type in categories_types])


async def validate_category(category):
    if category not in TYPES_FOR_CATEGORIES.keys():
        raise HTTPException(422, f"{category.capitalize()} isn't exist")


async def validate_type(category, typ):
    if typ not in TYPES_FOR_CATEGORIES[category]:
        raise HTTPException(422, f"Type {typ} can't be added to {category} category")


async def validate_categories_of_items(items_to_validate: AddTypesToItems):
    await asyncio.gather(*[validate_categories_of_item(item.categories_types) for item in items_to_validate.items])
