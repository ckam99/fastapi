import asyncio
from threading import Thread


class Pool:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.loop_runner = Thread(target=self.loop.run_forever)
        self.loop_runner.daemon = True
        self.loop_runner.start()

    def run(self, coro):
        return asyncio.run_coroutine_threadsafe(
            coro,
            self.loop,
        )

    async def shutdown(self):
        self.loop.stop()
        await self.loop.shutdown_asyncgens()
        await self.loop.aclose()

    def join(self):
        self.loop_runner.join()


pool: Pool = None


def setup():
    global pool

    if pool is not None:
        return

    pool = Pool()


def join_initialized():
    pool.loop_runner.join()


def join_uninitialized():
    pass


def run_initialized(coro):
    return pool.run(coro)


def run_uninitialized(coro):
    global run
    global join
    global shutdown
    setup()
    run = run_initialized
    join = join_initialized
    shutdown = shutdown_initialized
    return run_initialized(coro)


def shutdown_initialized():
    global run
    global join
    global shutdown
    global pool

    run = run_uninitialized
    join = shutdown_unitialized
    shutdown = shutdown_unitialized

    coro = pool.shutdown()
    pool = None
    return coro


def shutdown_unitialized():
    pass


run = run_uninitialized
join = join_uninitialized
shutdown = shutdown_unitialized
