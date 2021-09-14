import asyncio
from asgiref import sync

from . import pool


def gentask(corofunc):
    def wrapper(*args, **kwargs):
        coro = corofunc(*args, **kwargs)
        return asyncio.create_task(coro)
    return wrapper


def to_async(callback, as_task=True):
    corofunc = sync.sync_to_async(callback)

    if as_task and pool.pool:
        corofunc = gentask(corofunc)

    return corofunc
