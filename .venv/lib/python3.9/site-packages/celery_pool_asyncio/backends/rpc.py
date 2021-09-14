import asyncio
from celery.backends import rpc

from ..environment_variables import monkey_available


async def drain_events(self, timeout=None):
    if self._connection:
        coro = self._connection.drain_events(timeout=timeout)
        if coro:
            yield await coro
    elif timeout:
        await asyncio.sleep(timeout)


# --- celery.backends.rpc.ResultConsumer
ResultConsumer = rpc.ResultConsumer

if monkey_available('RPC.RESULTCONSUMER.DRAIN_EVENTS'):
    ResultConsumer._original_drain_events = ResultConsumer.drain_events
    ResultConsumer.drain_events = drain_events
