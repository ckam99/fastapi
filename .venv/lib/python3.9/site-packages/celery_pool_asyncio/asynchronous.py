import socket


async def _wait_for_pending(
    self,
    result,
    timeout=None,
    on_interval=None,
    on_message=None,
    **kwargs,
):
    self.on_wait_for_pending(result, timeout=timeout, **kwargs)
    prev_on_m, self.on_message = self.on_message, on_message
    try:
        async for _ in self.drain_events_until(
                result.on_ready, timeout=timeout,
                on_interval=on_interval):
            yield
    except socket.timeout:
        raise TimeoutError('The operation timed out.')
    finally:
        self.on_message = prev_on_m


async def wait_for_pending(
    self,
    result,
    callback=None,
    propagate=True,
    **kwargs,
):
    self._ensure_not_eager()
    async for _ in self._wait_for_pending(result, **kwargs):
        pass
    return result.maybe_throw(callback=callback, propagate=propagate)


async def drain_events_until(self, p, timeout=None, on_interval=None):
    async for _ in self.drainer.drain_events_until(
        p,
        timeout=timeout,
        on_interval=on_interval,
    ):
        yield
