from starlette.config import Config
from core.utils import load_models


config = Config('.env')

HOSTNAME = config('HOSTNAME', cast=str, default='0.0.0.0')
PORT = config('PORT', cast=int, default=8000)
DEBUG = config('DEBUG', cast=bool, default=True)

TIMEZONE = config('DEBUG', cast=str, default='UTC')
USE_TIMEZONE = config('USE_TIMEZONE', cast=bool, default=False)

ALLOWED_HOSTS = [
    "http://localhost",
    "http://localhost:8080",
]

DATABASE = {
    "postgresql": {
        "engine": "tortoise.backends.asyncpg",
        "credentials": {
            "host": config('DB_HOST', cast=str, default='localhost'),
            "database": config('DB_NAME', cast=str, default='dbname'),
            "port": config('DB_PORT', cast=int, default=5432),
            "user": config('DB_USER',  cast=str, default='postgres'),
            "password": config('DB_PASSWORD',  cast=str, default=''),
        }
    },
    "sqlite": "sqlite://db.sqlite3"
}

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE[config('DB_ENGINE', default='sqlite')]
    },
    "apps": {
        "models": {
            "models": [
                'models.base',
                *load_models()  # import models dynamacally
                # 'models.users',
                # 'models.stores',
                # 'models.products',
                # 'aerich.models'
            ],
            "default_connection": "default"
        }
    },
    "use_tz": USE_TIMEZONE,
    "timezone": TIMEZONE,
}


MEDIA_DIR = config('MEDIA_DIR', cast=str, default='media')
MEDIA_URL = config('MEDIA_URL', cast=str, default='media')


SECRET_KEY = config('SECRET_KEY', cast=str, default='')
JWT_TOKEN_ALGORITHM = config('JWT_TOKEN_ALGORITHM', cast=str, default='HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    'ACCESS_TOKEN_EXPIRE_MINUTES', cast=int, default=30)  # 30 minutes

AUTH_URL = config('AUTH_URL', cast=str, default='auth/login')


MAIL_USERNAME = config('MAIL_USERNAME', cast=str, default='')
MAIL_PASSWORD = config('MAIL_PASSWORD', cast=str, default='')
MAIL_FROM = config('MAIL_FROM', cast=str, default='noreply@example.com')
MAIL_PORT = config('MAIL_PORT', cast=int, default=2525)
MAIL_SERVER = config('MAIL_SERVER', cast=str, default='smtp.mailtrap.io')
MAIL_FROM_NAME = config('MAIL_FROM_NAME', cast=str, default='FastAPI')
MAIL_USE_TLS = config('MAIL_USE_TLS', cast=bool, default=False)
MAIL_USE_SSL = config('MAIL_USE_SSL', cast=bool, default=False)
MAIL_USE_CREDENTIALS = config('MAIL_USE_CREDENTIALS', cast=bool, default=False)
MAIL_VALIDATE_CERTS = config('MAIL_USE_CREDENTIALS', cast=bool, default=False)


# Celery and redis settings
CELERY_BROKER_URL = config(
    'CELERY_BROKER_URL', cast=str, default='redis://127.0.0.1:6379')
CELERY_RESULT_BACKEND = config(
    'CELERY_RESULT_BACKEND', cast=str, default='redis://127.0.0.1:6379')
CELERY_TASKS_REGISTER = [
    # ','.join(load_tasks()) # comment out this line to import automatically tasks
    'tasks.users'
]
