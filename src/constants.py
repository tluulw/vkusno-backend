from enum import Enum
from typing import Annotated

from sqlalchemy.orm import mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]


TYPES_FOR_CATEGORIES = {
    "new": [None],
    "popular": [None],
    "other": [None],
    "drink": ["hot", "cold", "juice", "milkshake"],
    "dessert": ["dessert", "icecream"],
    "snack": ["salad", "starter", "fries"],
    "cafe": ["dessert", "drink"],
    "burger": ["chicken", "beef", "roll", "fish"]
}
