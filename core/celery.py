from core.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, CELERY_TASKS_REGISTER
from celery import Celery
import time


celery = Celery(__name__, include=CELERY_TASKS_REGISTER)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


celery.autodiscover_tasks()


class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


''' Example tasks '''


@celery.task(name="create_test_task")
def create_test_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

# @shared_task(bind=True, base=BaseTaskWithRetry)
# def task_process_notification(self):
#     raise Exception()


# @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 5})
# def task_process_notification_3(self):
#     if not random.choice([0, 1]):
#         # mimic random error
#         raise Exception()
#     requests.post('https://httpbin.org/delay/5')


# @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_jitter=True, retry_kwargs={'max_retries': 5})
# def task_process_notification_2(self):
#     if not random.choice([0, 1]):
#         # mimic random error
#         raise Exception()
#     requests.post('https://httpbin.org/delay/5')
