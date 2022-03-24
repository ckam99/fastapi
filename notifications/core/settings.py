import os
from core.helpers import load_models

APP_NAME = 'Notification service'

KAFKA_HOST = os.environ.get('KAFKA_HOST', 'localhost:9092')
KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID', None)
KAFKA_TOPICS = [
    'user-deleted-event',
    'user-registred'
]

TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": "sqlite://db.sqlite3"
    },
    "apps": {
        "models": {
            "models": load_models(),
            "default_connection": "default",
        }
    },
}

MAIL_USERNAME = 'f10c9fcb8036ed'
MAIL_PASSWORD = "db94187020064b"
MAIL_BACKEND = 'smtp'
MAIL_SERVER = 'smtp.mailtrap.io'
MAIL_PORT = 2525
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USE_CREDENTIALS = True
MAIL_FROM = 'example@domain.com'
MAIL_FROM_NAME = 'App name'
MAIL_VALIDATE_CERTS = False
