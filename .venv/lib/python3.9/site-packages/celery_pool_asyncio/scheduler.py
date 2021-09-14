from celery import beat


class AsyncSchedulerMixin:
    async def apply_async(self, entry, producer=None, advance=True, **kwargs):
        # Update time-stamps and run counts before we actually execute,
        # so we have that done if an exception is raised (doesn't schedule
        # forever.)
        entry = self.reserve(entry) if advance else entry
        task = self.app.tasks.get(entry.task)

        try:
            entry_args = [
                v() if isinstance(v, beat.BeatLazyFunc) else v
                for v in (entry.args or [])
            ]
            entry_kwargs = {
                k: v() if isinstance(v, beat.BeatLazyFunc) else v
                for k, v in entry.kwargs.items()
            }

            if task:
                return await task.apply_async(
                    entry_args, entry_kwargs,
                    producer=producer,
                    **entry.options,
                )
            else:
                return await self.send_task(
                    entry.task, entry_args, entry_kwargs,
                    producer=producer,
                    **entry.options,
                )
        except Exception as exc:  # pylint: disable=broad-except
            msg = "Couldn't apply scheduled task {entry.name}: {exc}".format(
                entry=entry,
                exc=exc,
            )
            beat.reraise(
                beat.SchedulingError,
                beat.SchedulingError(msg),
                beat.sys.exc_info()[2]
            )
        finally:
            self._tasks_since_sync += 1
            if self.should_sync():
                self._do_sync()

    async def apply_entry(self, entry, producer=None):
        beat.info(
            'Scheduler: Sending due task %s (%s)',
            entry.name,
            entry.task,
        )

        try:
            coro = self.apply_async(
                entry=entry,
                producer=producer,
                advance=False,
            )
            result = await coro
        except Exception as exc:  # pylint: disable=broad-except
            beat.error(
                'Message Error: %s\n%s',
                exc,
                beat.traceback.format_stack(),
                exc_info=True,
            )
        else:
            beat.debug(
                '%s sent. id->%s',
                entry.task,
                result.id,
            )

    async def tick(
        self,
        event_t=beat.event_t,
        min=min,
        heappop=beat.heapq.heappop,
        heappush=beat.heapq.heappush,
    ):
        """Run a tick - one iteration of the scheduler.

        Executes one due task per call.

        Returns:
            float: preferred delay in seconds for next call.
        """
        adjust = self.adjust
        max_interval = self.max_interval

        should_populate_heap = (
            self._heap is None or
            not self.schedules_equal(self.old_schedulers, self.schedule)
        )

        if should_populate_heap:
            self.old_schedulers = beat.copy.copy(self.schedule)
            self.populate_heap()

        H = self._heap

        if not H:
            return max_interval

        event = H[0]
        entry = event[2]
        is_due, next_time_to_run = self.is_due(entry)
        if is_due:
            verify = heappop(H)
            if verify is event:
                next_entry = self.reserve(entry)
                await self.apply_entry(entry, producer=self.producer)
                heappush_event = event_t(
                    self._when(next_entry, next_time_to_run),
                    event[1],
                    next_entry,
                )
                heappush(H, heappush_event)
                return 0
            else:
                heappush(H, verify)
                return min(verify[0], max_interval)
        return min(
            adjust(next_time_to_run) or max_interval,
            max_interval,
        )


# XXX Doesn't work
# class Scheduler(AsyncSchedulerMixin, beat.Scheduler):
#     pass


class PersistentScheduler(AsyncSchedulerMixin, beat.PersistentScheduler):
    pass
