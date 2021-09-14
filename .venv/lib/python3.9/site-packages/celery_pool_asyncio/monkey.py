from .environment_variables import monkey_available
from .monkey_utils import to_async


# As early as possible
if monkey_available('SIGNAL.SEND'):
    from celery.utils.dispatch.signal import Signal
    from . import signal_send
    Signal.send = signal_send.send


from . import worker
from . import beat
from . import asynchronous
from . import tracer
from . import drainer

# --- celery.app.Celery
from celery.app import Celery

if monkey_available('CELERY.SEND_TASK'):
    # Celery task sending can be awaited
    Celery.send_task = to_async(Celery.send_task, True)


from celery.worker import worker as cwworker

# --- celery.worker.worker.WorkController
if monkey_available('WORKCONTROLLER.USE_EVENTLOOP'):
    cwworker.WorkController.should_use_eventloop = worker.should_use_eventloop

# --- celery.worker.worker.cpu_count
if monkey_available('WORKER.CPU_COUNT'):
    cwworker.cpu_count = lambda: 256


# --- celery.backends.asynchronous.BaseResultConsumer
from celery.backends.asynchronous import BaseResultConsumer

if monkey_available('BASERESULTCONSUMER.WAIT_FOR_PENDING'):
    BaseResultConsumer._wait_for_pending = asynchronous._wait_for_pending

if monkey_available('BASERESULTCONSUMER.DRAIN_EVENTS_UNTIL'):
    BaseResultConsumer.drain_events_until = asynchronous.drain_events_until

# --- celery.backends.asynchronous.AsyncBackendMixin
from celery.backends.asynchronous import AsyncBackendMixin

if monkey_available('ASYNCBACKENDMIXIN.WAIT_FOR_PENDING'):
    AsyncBackendMixin.wait_for_pending = asynchronous.wait_for_pending


if monkey_available('ALL_BACKENDS'):
    # Celery AsyncResult.get() can be awaited
    from . import backends  # noqa
    backends.__package__


# --- celery.beat.Service
Service = beat.beat.Service

if monkey_available('BEAT.SERVICE.START'):
    Service.start = beat.Service__start
    Service.async_start = beat.Service__async_start
    Service.async_run = beat.Service__async_run

if monkey_available('BEAT.SERVICE.STOP'):
    Service.stop = beat.Service__stop


# --- celery.app.trace.build_tracer
if monkey_available('BUILD_TRACER'):
    tracer.trace.build_tracer = tracer.build_async_tracer

# --- kombu.utils.compat
from kombu.utils import compat  # noqa

if monkey_available('KOMBU.UTILS.COMPAT'):
    compat._detect_environment = drainer._detect_environment
