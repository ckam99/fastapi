import os


KAFKA_HOST = 'localhost:9092'
KAFKA_GROUP_ID = 'sprintboot-kafka-fastapi'
KAFKA_TOPICS = ['message-create']

TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": "sqlite://db.sqlite3"
    },
    "apps": {
        "models": {
            "models": ["models.message"],
            "default_connection": "default",
        }
    },
}
