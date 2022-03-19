import os


PULSAR_HOST = os.environ.get('PULSAR_HOST', 'pulsar://localhost:6650')


TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": 'sqlite://db.sqlite3'
    },
    "apps": {
        "models": {
            "models": ["events.models"],
            "default_connection": "default",
        }
    },
}
