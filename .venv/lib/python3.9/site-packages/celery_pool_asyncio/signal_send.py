import asyncio
from celery.utils.dispatch.signal import (
    NO_RECEIVERS,
    sys,
    logger,
)
from .async_to_sync import AsyncToSync


def handle_error(self, receiver, exc):
    if not hasattr(exc, '__traceback__'):
        exc.__traceback__ = sys.exc_info()[2]
    logger.exception('Signal handler %r raised: %r', receiver, exc)
    return (receiver, exc)


def send_iter(self, sender, **named):
    if not self.receivers or \
            self.sender_receivers_cache.get(sender) is NO_RECEIVERS:
        return

    for receiver in self._live_receivers(sender):
        try:
            if asyncio.iscoroutinefunction(receiver):
                coro = receiver(signal=self, sender=sender, **named)
                waiter = AsyncToSync(coro)
                waiter()  # blocking

                if waiter.error:
                    yield handle_error(self, receiver, waiter.result)
                    continue

                yield (receiver, waiter.result)
            else:
                response = receiver(signal=self, sender=sender, **named)
                yield (receiver, response)

        except Exception as exc:  # pylint: disable=broad-except
            yield handle_error(self, receiver, exc)


def send(self, sender, **named):
    """Send signal from sender to all connected receivers.

    If any receiver raises an error, the error propagates back through
    send, terminating the dispatch loop, so it is quite possible to not
    have all receivers called if a raises an error.

    Arguments:
        sender (Any): The sender of the signal.
            Either a specific object or :const:`None`.
        **named (Any): Named arguments which will be passed to receivers.

    Returns:
        List: of tuple pairs: `[(receiver, response), … ]`.
    """
    return list(send_iter(self, sender, **named))
