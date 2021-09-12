from starlette.background import BackgroundTasks
from tortoise.signals import pre_save, pre_delete, post_delete, post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient
from .models import User
from .tasks import send_confirmation_email


# @pre_save(User)
# async def signal_pre_save(
#     sender: "Type[User]", instance: User, using_db, update_fields
# ) -> None:
#     print(sender, instance, using_db, update_fields)


@post_save(User)
async def signal_post_save(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str],
    # background_task: BackgroundTasks
) -> None:
    if instance.email_confirmed_at is None:
        send_confirmation_email.delay(instance.email)
        # create_task.delay(2, 4, 6)
    # background_task.add_task(send_confirmation_email, instance)


# @pre_delete(User)
# async def signal_pre_delete(
#     sender: "Type[User]", instance: User, using_db: "Optional[BaseDBAsyncClient]"
# ) -> None:
#     print(sender, instance, using_db)


# @post_delete(User)
# async def signal_post_delete(
#     sender: "Type[User]", instance: User, using_db: "Optional[BaseDBAsyncClient]"
# ) -> None:
#     print(sender, instance, using_db)
