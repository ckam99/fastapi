import os
import time
from core.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from celery import Celery


celery = Celery(__name__, include=['base.tasks'])
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


celery.autodiscover_tasks()
