import asyncio
import traceback
from celery import beat

from . import pool


async def Service__async_run(self):
    while not self._is_shutdown.is_set():
        interval = await self.scheduler.tick()
        if interval and interval > 0.0:
            beat.debug(
                'beat: Waking up %s.',
                beat.humanize_seconds(interval, prefix='in '),
            )
            await asyncio.sleep(interval)
            if self.scheduler.should_sync():
                self.scheduler._do_sync()


async def Service__async_start(self):
    try:
        await self.async_run()
    except (KeyboardInterrupt, SystemExit):
        self._is_shutdown.set()
    finally:
        traceback.print_exc()
        self.sync()


def Service__start(self, embedded_process=False):
    beat.info('beat: Starting...')
    beat.debug(
        'beat: Ticking with max interval->%s',
        beat.humanize_seconds(self.scheduler.max_interval),
    )

    beat.signals.beat_init.send(sender=self)
    if embedded_process:
        beat.signals.beat_embedded_init.send(sender=self)
        beat.platforms.set_process_title('celery beat')

    coro = self.async_start()
    pool.run(coro)
    pool.join()


def Service__stop(self, wait=False):
    beat.info('beat: Shutting down...')
    self._is_shutdown.set()
    coro = pool.pool and pool.pool.shutdown()
    coro and pool.pool.run(coro)
    wait and pool.join()  # block until shutdown done.
