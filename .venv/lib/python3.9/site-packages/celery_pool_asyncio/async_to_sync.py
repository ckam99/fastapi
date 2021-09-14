from threading import Event
from . import pool


class AsyncToSync:
    __slots__ = (
        'coro',
        'event',
        'error',
        'result',
    )

    def __init__(self, coro):
        self.coro = coro
        self.event = Event()

    def __call__(self):
        coro = self.__wrapper()
        pool.run(coro)
        self.event.wait()

    async def __wrapper(self):
        try:
            self.result = await self.coro
            self.error = False
        except Exception as e:
            self.result = e
            self.error = True
        finally:
            self.event.set()
