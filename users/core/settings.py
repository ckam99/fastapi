import os
from core.helpers import load_models

KAFKA_HOST = os.environ.get('KAFKA_HOST', 'localhost:9092')
KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID', None)
KAFKA_TOPICS = [
    'notification-created-event',
    'notification-updated-event',
    'notification-deleted-event',
    'user-created-event',
    'user-updated-event',
    'user-deleted-event'
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
