from core.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, CELERY_TASKS_REGISTER
from celery import Celery


celery = Celery(__name__, include=CELERY_TASKS_REGISTER)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


celery.autodiscover_tasks()
