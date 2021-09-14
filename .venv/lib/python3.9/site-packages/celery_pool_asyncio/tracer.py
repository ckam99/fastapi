import os
import logging
import asyncio


from celery import canvas
from celery.app import trace
from celery.exceptions import (
    SoftTimeLimitExceeded,
    TimeoutError as CeleryTimeoutError,
)
from .exceptions import SoftRevoked
from . import coro_utils


logger = trace.logger
_does_info = logger.isEnabledFor(logging.INFO)

_task_stack = trace._task_stack
saferepr = trace.saferepr
group = trace.group
signals = trace.signals

Ignore = trace.Ignore
InvalidTaskError = trace.InvalidTaskError
Reject = trace.Reject
Retry = trace.Retry
EncodeError = trace.EncodeError
ExceptionInfo = trace.ExceptionInfo

STARTED = trace.STARTED
SUCCESS = trace.SUCCESS
IGNORED = trace.IGNORED
REJECTED = trace.REJECTED
RETRY = trace.RETRY
FAILURE = trace.FAILURE
EXCEPTION_STATES = trace.EXCEPTION_STATES

prerun_receivers = signals.task_prerun.receivers
postrun_receivers = signals.task_postrun.receivers
success_receivers = signals.task_success.receivers

send_prerun = signals.task_prerun.send
send_postrun = signals.task_postrun.send
send_success = signals.task_success.send

push_task = _task_stack.push
pop_task = _task_stack.pop

signature = canvas.maybe_signature  # maybe_ does not clone if already


def build_async_tracer(
    name,
    task,
    loader=None,
    hostname=None,
    store_errors=True,
    Info=trace.TraceInfo,
    eager=False,
    propagate=False,
    app=None,
    monotonic=trace.monotonic,
    trace_ok_t=trace.trace_ok_t,
    IGNORE_STATES=trace.IGNORE_STATES,
):
    """Return a function that traces task execution.

    Catches all exceptions and updates result backend with the
    state and result.

    If the call was successful, it saves the result to the task result
    backend, and sets the task status to `"SUCCESS"`.

    If the call raises :exc:`~@Retry`, it extracts
    the original exception, uses that as the result and sets the task state
    to `"RETRY"`.

    If the call results in an exception, it saves the exception as the task
    result, and sets the task state to `"FAILURE"`.

    Return a function that takes the following arguments:

        :param uuid: The id of the task.
        :param args: List of positional args to pass on to the function.
        :param kwargs: Keyword arguments mapping to pass on to the function.
        :keyword request: Request dict.

    """
    # noqa: C901
    # pylint: disable=too-many-statements

    # If the task doesn't define a custom __call__ method
    # we optimize it away by simply calling the run method directly,
    # saving the extra method call and a line less in the stack trace.
    fun = task if trace.task_has_custom(task, '__call__') else task.run

    loader = loader or app.loader
    backend = task.backend
    ignore_result = task.ignore_result
    track_started = task.track_started
    track_started = not eager and (task.track_started and not ignore_result)
    publish_result = not eager and not ignore_result
    hostname = hostname or trace.gethostname()
    inherit_parent_priority = app.conf.task_inherit_parent_priority

    loader_task_init = loader.on_task_init
    loader_cleanup = loader.on_process_cleanup

    task_on_success = None
    task_after_return = None
    if trace.task_has_custom(task, 'on_success'):
        task_on_success = task.on_success
    if trace.task_has_custom(task, 'after_return'):
        task_after_return = task.after_return

    store_result = backend.store_result
    mark_as_done = backend.mark_as_done
    backend_cleanup = backend.process_cleanup

    pid = os.getpid()

    request_stack = task.request_stack
    push_request = request_stack.push
    pop_request = request_stack.pop
    resultrepr_maxsize = task.resultrepr_maxsize

    def on_error(request, exc, uuid, state=FAILURE, call_errbacks=True):
        if propagate:
            raise
        EI = Info(state, exc)
        R = EI.handle_error_state(
            task, request, eager=eager, call_errbacks=call_errbacks,
        )
        return EI, R, EI.state, EI.retval

    async def trace_task(uuid, args, kwargs, request=None):
        # R      - is the possibly prepared return value.
        # I      - is the Info object.
        # T      - runtime
        # Rstr   - textual representation of return value
        # retval - is the always unmodified return value.
        # state  - is the resulting task state.

        # This function is very long because we've unrolled all the calls
        # for performance reasons, and because the function is so long
        # we want the main variables (I, and R) to stand out visually from the
        # the rest of the variables, so breaking PEP8 is worth it ;)
        R = I = T = Rstr = retval = state = None
        task_request = None
        time_start = monotonic()
        try:
            try:
                kwargs.items
            except AttributeError:
                raise InvalidTaskError(
                    'Task keyword arguments is not a mapping')
            push_task(task)
            task_request = trace.Context(
                request or {},
                args=args,
                called_directly=False,
                kwargs=kwargs,
            )
            root_id = task_request.root_id or uuid
            task_priority = task_request.delivery_info.get('priority') if \
                inherit_parent_priority else None
            push_request(task_request)
            try:
                # -*- PRE -*-
                if prerun_receivers:
                    send_prerun(sender=task, task_id=uuid, task=task,
                                args=args, kwargs=kwargs)
                loader_task_init(uuid, task)
                if track_started:
                    store_result(
                        uuid, {'pid': pid, 'hostname': hostname}, STARTED,
                        request=task_request,
                    )

                # -*- TRACE -*-
                try:
                    coro = fun(*args, **kwargs)
                    coro_task = asyncio.create_task(coro)

                    waiter = asyncio.wait(
                        [coro_task],
                        timeout=task.soft_time_limit,
                    )

                    waiter_task = asyncio.create_task(waiter)

                    try:
                        await waiter_task

                        if coro_task.done():
                            R = retval = coro_task.result()
                        else:
                            R = retval = await coro_utils.send_exception(
                                coro,
                                SoftTimeLimitExceeded(),
                            )
                            await coro_utils.await_anyway(coro_task)

                    except asyncio.CancelledError as exc:
                        waiter_task.cancel()
                        coro_task.cancel()
                        waiter.close()
                        coro.close()
                        exc = CeleryTimeoutError(exc)
                        exc = str(exc)
                        I, R, state, retval = on_error(task_request, exc, uuid)

                    except SoftRevoked:
                        R = retval = await coro_utils.send_exception(
                            coro,
                            SoftTimeLimitExceeded(),
                        )
                        await coro_utils.await_anyway(coro_task)

                    state = SUCCESS
                except Reject as exc:
                    waiter_task.cancel()
                    coro_task.cancel()
                    try:
                        await coro_utils.await_anyway(coro_task)
                    except asyncio.CancelledError:
                        pass

                    I = Info(REJECTED, exc)
                    R = ExceptionInfo(internal=True)
                    state, retval = I.state, I.retval
                    I.handle_reject(task, task_request)
                except Ignore as exc:
                    I = Info(IGNORED, exc)
                    R = ExceptionInfo(internal=True)
                    state, retval = I.state, I.retval
                    I.handle_ignore(task, task_request)
                except Retry as exc:
                    I, R, state, retval = on_error(
                        task_request, exc, uuid, RETRY, call_errbacks=False)
                except SoftTimeLimitExceeded as exc:
                    I, R, state, retval = on_error(task_request, exc, uuid)
                except Exception as exc:
                    coro.close()
                    await coro_utils.await_anyway(waiter_task)
                    I, R, state, retval = on_error(task_request, exc, uuid)
                except BaseException:
                    raise
                else:
                    try:
                        # callback tasks must be applied before the result is
                        # stored, so that result.children is populated.

                        # groups are called inline and will store trail
                        # separately, so need to call them separately
                        # so that the trail's not added multiple times :(
                        # (Issue #1936)
                        callbacks = task.request.callbacks
                        if callbacks:
                            if len(task.request.callbacks) > 1:
                                sigs, groups = [], []
                                for sig in callbacks:
                                    sig = signature(sig, app=app)
                                    if isinstance(sig, group):
                                        groups.append(sig)
                                    else:
                                        sigs.append(sig)
                                for group_ in groups:
                                    group_.apply_async(
                                        (retval,),
                                        parent_id=uuid, root_id=root_id,
                                        priority=task_priority
                                    )
                                if sigs:
                                    group(sigs, app=app).apply_async(
                                        (retval,),
                                        parent_id=uuid, root_id=root_id,
                                        priority=task_priority
                                    )
                            else:
                                signature(callbacks[0], app=app).apply_async(
                                    (retval,), parent_id=uuid, root_id=root_id,
                                    priority=task_priority
                                )

                        # execute first task in chain
                        chain = task_request.chain
                        if chain:
                            _chsig = signature(chain.pop(), app=app)
                            _chsig.apply_async(
                                (retval,), chain=chain,
                                parent_id=uuid, root_id=root_id,
                                priority=task_priority
                            )
                        mark_as_done(
                            uuid, retval, task_request, publish_result,
                        )
                    except EncodeError as exc:
                        I, R, state, retval = on_error(task_request, exc, uuid)
                    else:
                        Rstr = saferepr(R, resultrepr_maxsize)
                        T = monotonic() - time_start
                        if task_on_success:
                            task_on_success(retval, uuid, args, kwargs)
                        if success_receivers:
                            send_success(sender=task, result=retval)
                        if _does_info:
                            task_name = trace.get_task_name(task_request, name)
                            trace.info(trace.LOG_SUCCESS, {
                                'id': uuid,
                                'name': task_name,
                                'return_value': Rstr,
                                'runtime': T,
                            })

                # -* POST *-
                if state not in trace.IGNORE_STATES:
                    if task_after_return:
                        task_after_return(
                            state, retval, uuid, args, kwargs, None,
                        )
            finally:
                await coro_utils.await_anyway(coro_task)
                try:
                    if postrun_receivers:
                        send_postrun(sender=task, task_id=uuid, task=task,
                                     args=args, kwargs=kwargs,
                                     retval=retval, state=state)
                finally:
                    pop_task()
                    pop_request()
                    if not eager:
                        try:
                            backend_cleanup()
                            loader_cleanup()
                        except (KeyboardInterrupt, SystemExit, MemoryError):
                            raise
                        except Exception as exc:
                            logger.error('Process cleanup failed: %r', exc,
                                         exc_info=True)
        except MemoryError:
            raise
        except Exception as exc:
            if eager:
                raise
            R = trace.report_internal_error(task, exc)
            if task_request is not None:
                I, _, _, _ = on_error(task_request, exc, uuid)
        return trace_ok_t(R, I, T, Rstr)

    return trace_task
