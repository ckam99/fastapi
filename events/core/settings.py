import os
from core.helpers import load_models


APP_NAME = 'Events service'

KAFKA_HOST = os.environ.get('KAFKA_HOST', 'localhost:9092')
KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID', None)
KAFKA_TOPICS = [
    'user-created-event',
    'user-updated-event',
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
