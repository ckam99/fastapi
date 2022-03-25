from starlette.config import Config
from core.utils import load_models
import os

config = Config('.env')

DB_NAME = config('DB_NAME', default='')
DB_USER = config('DB_USER', default='')
MY_SURNAME = config('MY_SURNAME', default='')

HOSTNAME = os.environ.get('HOSTNAME', '0.0.0.0')
PORT = os.environ.get('PORT',  8000)
DEBUG = os.environ.get('DEBUG', True)

TIMEZONE = os.environ.get('DEBUG', 'UTC')
USE_TIMEZONE = os.environ.get('USE_TIMEZONE', False)

ALLOWED_HOSTS = [
    "http://localhost",
    "http://localhost:8080",
]

DATABASE = {
    "postgresql": {
        "engine": "tortoise.backends.asyncpg",
        "credentials": {
            "host": os.environ.get('DB_HOST', 'localhost'),
            "database": os.environ.get('DB_NAME', 'dbname'),
            "port": os.environ.get('DB_PORT', 5432),
            "user": os.environ.get('DB_USER', 'postgres'),
            "password": os.environ.get('DB_PASSWORD', ''),
        }
    },
    "sqlite": "sqlite://db.sqlite3"
}

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE[os.environ.get('DB_ENGINE', 'sqlite')]
    },
    "apps": {
        "models": {
            "models": [
                *load_models(),  # import models dynamacally
                # 'models.auth',
                "aerich.models"
            ],
            "default_connection": "default"
        }
    },
    "use_tz": USE_TIMEZONE,
    "timezone": TIMEZONE,
}


MEDIA_DIR = os.environ.get('MEDIA_DIR', 'media')
MEDIA_URL = os.environ.get('MEDIA_URL', 'media')


SECRET_KEY = os.environ.get('SECRET_KEY', '')
JWT_TOKEN_ALGORITHM = os.environ.get('JWT_TOKEN_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get(
    'ACCESS_TOKEN_EXPIRE_MINUTES', 30)  # 30 minutes

AUTH_URL = os.environ.get('AUTH_URL', 'auth/login')


MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
MAIL_FROM = os.environ.get('MAIL_FROM', 'noreply@example.com')
MAIL_PORT = os.environ.get('MAIL_PORT', 2525)
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.mailtrap.io')
MAIL_FROM_NAME = os.environ.get('MAIL_FROM_NAME', 'FastAPI')
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', False)
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', False)
MAIL_USE_CREDENTIALS = os.environ.get('MAIL_USE_CREDENTIALS', False)
MAIL_VALIDATE_CERTS = os.environ.get('MAIL_USE_CREDENTIALS', False)


# Celery and redis settings
CELERY_BROKER_URL = os.environ.get(
    'CELERY_BROKER_URL', 'redis://127.0.0.1:6379')
CELERY_RESULT_BACKEND = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379')
CELERY_TASKS_REGISTER = [
    # ','.join(load_tasks()) # comment out this line to import automatically tasks
    'tasks.auth'
]
