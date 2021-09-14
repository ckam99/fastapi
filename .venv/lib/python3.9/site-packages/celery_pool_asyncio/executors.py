import sys
import asyncio
from threading import Semaphore
from celery.concurrency import base
from billiard.einfo import ExceptionInfo
from celery.app import trace
from kombu.serialization import loads as loads_message

from celery.exceptions import Reject
from .exceptions import SoftRevoked

from celery.worker import control
original_control__revoke = control.revoke

register_revoke = control.control_command(
    variadic='task_id',
    signature='[id1 [id2 [... [idN]]]]',
    name='revoke',
)

from . import pool  # noqa
from . import coro_utils   # noqa


class TaskPool(base.BasePool):
    signal_safe = False
    is_green = False
    task_join_will_block = False

    def on_start(self):
        register_revoke(self.control_revoke)
        control.revoke = self.control_revoke

        self.semaphore = Semaphore(self.limit - 1)
        self.stopping = False
        self.coroutines = {}
        self.tasks = {}

        coro = self.after_start()
        pool.run(coro)

    async def after_start(self):
        pass

    def on_stop(self):
        """Gracefully stop the pool."""
        self.stopping = True
        self.try_stop()
        pool.pool.join()
        control.revoke = original_control__revoke

    def try_stop(self):
        """Shutdown should be happend after last task has been done"""
        if not self.coroutines:
            coro = pool.pool and pool.pool.shutdown()
            coro and pool.run(coro)

    def on_terminate(self):
        """Force terminate the pool."""
        for task_id, coro in self.coroutines.items():
            coro.close()

        pool.loop.stop()
        yield from pool.loop.shutdown_asyncgens()
        pool.loop.close()
        pool.pool.stop()
        control.revoke = original_control__revoke

    control_revoke__exceptions = (
        SoftRevoked,
        Reject,
    )

    def control_revoke(
        self,
        state,
        task_id,
        terminate=False,
        signal=None,
        **kwargs,
    ):
        exc = self.control_revoke__exceptions[terminate]
        task_ids = control.maybe_list(task_id) or []
        task_ids = set(task_ids)
        for task_id in task_ids:
            self.send_exception(task_id, exc)

    def send_exception(self, task_id, exc):
        timeout_coro = self.do_async_soft_timeout(
            task_id=task_id,
            exc=exc,
        )
        pool.run(timeout_coro)

    async def do_async_soft_timeout(self, task_id, exc):
        coro = self.coroutines[task_id]
        await coro_utils.send_exception(coro, exc)

    def restart(self):
        self.on_stop()
        self.on_start()

    def on_apply(
        self,
        target,
        args,
        kwargs=None,
        **options,
    ):
        """Looks crazy"""
        (
            task,
            task_uuid,
            request,
            body,
            content_type,
            content_encoding,
        ) = args

        _, accept, hostname = trace._localized

        (
            task_args,
            task_kwargs,
            task_embed,
        ) = loads_message(
            body,
            content_type,
            content_encoding,
            accept=accept,
        )

        task_embed = task_embed or {}

        request.update({
            'args': args,
            'kwargs': kwargs,
            'hostname': hostname,
            'is_eager': False,
        }, **task_embed)

        target_task = self.app.tasks[task]

        coro = self.task_coro(
            target_task,
            task_uuid,
            task_args,
            task_kwargs,
            request,
            **options,
        )

        self.coroutines[task_uuid] = coro
        pool.run(coro)
        self.semaphore.acquire()

    async def task_coro(
        self,
        coro_function,
        task_uuid,
        coro_args,
        coro_kwargs,
        request,
        accept_callback=None,
        callback=None,  # on_success
        timeout_callback=None,
        error_callback=None,
        soft_timeout=None,
        timeout=None,
        **options,
    ):
        try:
            accept_callback and accept_callback(
                base.os.getpid(),
                base.monotonic(),
            )

            trace_ok_coro = coro_function.__trace__(
                task_uuid,
                coro_args,
                coro_kwargs,
                request,
            )

            try:
                retval = await asyncio.wait_for(trace_ok_coro, timeout)
                callback and callback((0, retval, base.monotonic()))
            except asyncio.TimeoutError:
                timeout_callback and timeout_callback(
                    soft_timeout,
                    timeout,
                )
                raise

        except Exception as e:
            type_, _, tb = sys.exc_info()
            reason = e
            EI = ExceptionInfo((type_, reason, tb))
            error_callback and error_callback(
                EI,
                base.monotonic(),
            )

        finally:
            self.semaphore.release()
            self.coroutines.pop(task_uuid)
            self.stopping and self.try_stop()
