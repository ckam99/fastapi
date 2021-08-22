from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv('.env')

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = '56c754aa365a357c7242b15f23b7187ac749a6ec28e9f2775c49b498c5d42825'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: 30

AUTH_URL = 'auth/login'

ALLOWED_HOSTS = []

TEMPLATE_FOLDER = 'base/templates'

DATABASE = {
    "connections": {
        "default": "sqlite://db.sqlite3"
    },
    "apps": {
        "models": {
            "models": [
                "base.models",
                "polls.models",
                "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}

STATIC_DIR = BASE_DIR.joinpath('base/static')
MEDIA_DIR = 'media'


# DATABASE = {
#     "connections": {
#         "default": {
#             "engine": "tortoise.backends.asyncpg",
#             "credentials": {
#                 "host": "localhost",
#                 "port": "5432",
#                 "user": "ckam",
#                 "password": "123456",
#                 "database": "fastapi"
#             }
#         },
#         "sqlite": "sqlite://db.sqlite3"
#     },
#     "apps": {
#         "models": {
#             "models": [
#                 "accounts.models",
#                 "blog.models",
#                 "events.models",
#                 "aerich.models"
#             ],
#             "default_connection": "sqlite"
#         }
#     }
# }

MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
MAIL_FROM = os.environ.get('MAIL_FROM', 'noreply@example.com')
MAIL_PORT = os.environ.get('MAIL_PORT', 2525)
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.mailtrap.io')
MAIL_FROM_NAME = os.environ.get('MAIL_FROM_NAME', 'FastAPI')
MAIL_TLS = os.environ.get('MAIL_TLS', False)
MAIL_SSL = os.environ.get('MAIL_SSL', False)
USE_CREDENTIALS = os.environ.get('USE_CREDENTIALS', False)
