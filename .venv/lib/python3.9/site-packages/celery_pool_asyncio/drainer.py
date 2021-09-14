import socket
import celery.backends.asynchronous as asynchronous


@asynchronous.register_drainer('asyncio')
class asyncioDrainer(asynchronous.Drainer):
    async def drain_events_until(
        self,
        p,
        timeout=None,
        on_interval=None,
        wait=None,
    ):
        wait = wait or self.result_consumer.drain_events
        time_start = asynchronous.monotonic()

        while 1:
            # Total time spent may exceed a single call to wait()
            if timeout and asynchronous.monotonic() - time_start >= timeout:
                raise socket.timeout()
            try:
                yield await self.wait_for(p, wait, timeout=1)
            except socket.timeout:
                pass
            if on_interval:
                on_interval()
            if p.ready:  # got event on the wanted channel.
                break

    async def wait_for(self, p, wait, timeout=None):
        async for _ in wait(timeout=timeout):
            pass


def _detect_environment():
    return 'asyncio'
