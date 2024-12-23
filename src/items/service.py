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
