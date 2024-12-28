# Service - Data Access Layer(DAL). Для бизнес логики, связанной с item_size
from src.items_sizes.models import ItemSizeOrm
from src.items_sizes.schemas import ItemSizeAdd


# Добавляем item_size в сессию
async def _add_sizes(sizes: list[ItemSizeAdd], session):
    # Функция принимает список из размеров, сессию и добавляет размеры в сессию
    items_sizes = [ItemSizeOrm(**size.model_dump()) for size in sizes]
    session.add_all(items_sizes)