from celery.backends import amqp

from ..monkey_utils import to_async
from ..environment_variables import monkey_available


async def get_many(
    self,
    task_ids,
    timeout=None,
    no_ack=True,
    on_message=None,
    on_interval=None,
    now=amqp.monotonic,
    getfields=amqp.itemgetter('status', 'task_id'),
    READY_STATES=amqp.states.READY_STATES,
    PROPAGATE_STATES=amqp.states.PROPAGATE_STATES,
    **kwargs,
):
    with self.app.pool.acquire_channel(block=True) as (conn, channel):
        ids = set(task_ids)
        cached_ids = set()
        mark_cached = cached_ids.add
        for task_id in ids:
            try:
                cached = self._cache[task_id]
            except KeyError:
                pass
            else:
                if cached['status'] in READY_STATES:
                    yield task_id, cached
                    mark_cached(task_id)
        ids.difference_update(cached_ids)
        results = amqp.deque()
        push_result = results.append
        push_cache = self._cache.__setitem__
        decode_result = self.meta_from_decoded

        def _on_message(message):
            body = decode_result(message.decode())
            if on_message is not None:
                on_message(body)
            state, uid = getfields(body)
            if state in READY_STATES:
                push_result(body) \
                    if uid in task_ids else push_cache(uid, body)

        bindings = self._many_bindings(task_ids)
        with self.Consumer(channel, bindings, on_message=_on_message,
                           accept=self.accept, no_ack=no_ack):
            wait = conn.drain_events
            popleft = results.popleft
            while ids:
                await wait(timeout=timeout)
                while results:
                    state = popleft()
                    task_id = state['task_id']
                    ids.discard(task_id)
                    push_cache(task_id, state)
                    yield task_id, state
                if on_interval:
                    on_interval()


# --- celery.backends.amqp.AMQPBackend
AMQPBackend = amqp.AMQPBackend

if monkey_available('AMQPBACKEND.DRAIN_EVENTS'):
    AMQPBackend.drain_events = to_async(AMQPBackend.drain_events, False)

if monkey_available('AMQPBACKEND.GET_MANY'):
    AMQPBackend.get_many = get_many
