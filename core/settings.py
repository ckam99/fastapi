from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv('.env')

APP_NAME = 'FastAPI'
APP_VERSION = 1.0
APP_DESCRIPTION = """
FastAPI
## Heading
**Hello World **
"""

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get('DEBUG', True)

TIMEZONE = 'UTC'

SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'your_secret')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: 30

AUTH_URL = 'auth/login'

ALLOWED_HOSTS = []

TEMPLATE_FOLDER = 'resources/templates'

DATABASES = {
    'postgresql': "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        os.environ.get('DB_USER', 'postgres'),
        os.environ.get('DB_PASSWORD', 'your_password'),
        os.environ.get('DB_HOST', 'localhost'),
        os.environ.get('DB_PORT', 5432),
        os.environ.get('DB_NAME', 'test')
    ),
    "sqlite": "sqlite:///db.sqlite3"
}

STATIC_DIR = BASE_DIR.joinpath('resources/static')
MEDIA_DIR = 'media'

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
