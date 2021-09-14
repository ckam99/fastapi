async def await_anyway(aiotask):
    if aiotask is None:
        return

    if aiotask.done():
        return

    aiotask.cancel()
    try:
        await aiotask
        # "RuntimeError: cannot reuse already awaited coroutine"
    except RuntimeError:
        # but should
        pass


async def send_exception(coro, exception):
    try:
        await coro.throw(exception)
    except StopIteration as e:
        return e.value
