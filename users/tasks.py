from producers import UserProducer


async def user_create_task(data):
    UserProducer().user_created(data)


async def user_update_task(data):
    UserProducer().user_updated(data)


async def user_remove_task(data):
    UserProducer().user_removed(data)
