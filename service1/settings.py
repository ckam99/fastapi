import os


TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database":  os.environ.get('DB_NAME', 'fastapi'),
                "host": os.environ.get('DB_HOST', 'localhost'),
                "password":  os.environ.get('DB_PASSWORD', 'postgres'),
                "port": os.environ.get('DB_PORT', 5432),
                "user":  os.environ.get('DB_USER', 'postgres'),
                # "ssl": ctx  # Here we pass in the SSL context
            }
        }
    },
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        }
    },
}
