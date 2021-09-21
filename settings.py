import os
from core.utils import load_models, load_tasks
from dotenv import load_dotenv

load_dotenv('.env')

SECRET_KEY = os.getenv('SECRET_KEY', '09d25e094faa6ca2556c818166b7a')
JWT_TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes

TIMEZONE = 'Europe/Moscow'

# DATABASE_URL = 'sqlite://db.sqlite3'
DATABASE_URL = "postgres://{}:{}@{}:{}/{}".format(
    os.environ.get('DB_USER'),
    os.environ.get('DB_PASSWORD'),
    os.environ.get('DB_HOST', 'localhost'),
    os.environ.get('DB_PORT'),
    os.environ.get('DB_NAME')
)
TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": [
                ','.join(load_models()),
                # you can also import manually "models.auth",
                "aerich.models"
            ],
            "default_connection": "default"
        }
    },
    "use_tz": False,
    "timezone": TIMEZONE,
}
DATABASE_GENERATE_SCHEMAS = True


MEDIA_DIR = 'media'
MEDIA_URL = 'media'

MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
MAIL_FROM = os.environ.get('MAIL_FROM', 'noreply@example.com')
MAIL_PORT = os.environ.get('MAIL_PORT', 2525)
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.mailtrap.io')
MAIL_FROM_NAME = os.environ.get('MAIL_FROM_NAME', 'FastAPI')
MAIL_TLS = os.environ.get('MAIL_TLS', False)
MAIL_SSL = os.environ.get('MAIL_SSL', False)
USE_CREDENTIALS = os.environ.get('USE_CREDENTIALS', False)


# Celery and redis settings
CELERY_BROKER_URL = os.environ.get(
    'CELERY_BROKER_URL', 'redis://127.0.0.1:6379')
CELERY_RESULT_BACKEND = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379')
CELERY_TASKS_REGISTER = [
    ','.join(load_tasks())
]
