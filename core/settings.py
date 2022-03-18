

KAFKA_HOST = 'localhost:9092'

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
