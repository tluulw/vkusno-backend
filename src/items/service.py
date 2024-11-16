from src.items.schemas import ItemAdd


async def save_image_to_s3(image):

    # Save image into s3
    # Every image has own hash

    pass


async def item_serialize(position: ItemAdd):
    # src = await save_image_to_s3(position.image)
    # # Save image into s3
    # # Every image has own hash
    #
    # position.image = src  # src to image in s3

    return position


async def upload_items_to_json(items: list):
    json_with_items = {}

    for item in items:
        json_with_items[item[0]] = {'title': item[1],
                                    'image': item[2],
                                    'description': item[3],
                                    'price': item[4],
                                    'size': item[5]}

    return json_with_items
