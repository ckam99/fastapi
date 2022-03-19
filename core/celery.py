from core.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, CELERY_TASKS_REGISTER
from celery import Celery
import time


celery = Celery(__name__, include=CELERY_TASKS_REGISTER)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


celery.autodiscover_tasks()


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
