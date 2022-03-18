from tortoise.signals import pre_save, pre_delete, post_delete, post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient
from models.message import Message


@pre_save(Message)
async def signal_pre_save(
    sender: "Type[Message]", instance: Message, using_db, update_fields
) -> None:
    print('message_pre_save: ', sender, instance, using_db, update_fields)


@post_save(Message)
async def signal_post_save(
    sender: "Type[Message]",
    instance: Message,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str],
) -> None:
    print('message_post_save: ', sender, instance, using_db, update_fields)


@pre_delete(Message)
async def signal_pre_delete(
    sender: "Type[Message]", instance: Message, using_db: "Optional[BaseDBAsyncClient]"
) -> None:
    print('message_pre_delete: ', sender, instance, using_db)


@post_delete(Message)
async def signal_post_delete(
    sender: "Type[Message]", instance: Message, using_db: "Optional[BaseDBAsyncClient]"
) -> None:
    print('message_post_delete: ', sender, instance, using_db)
