
DEBUG = True

SECRET_KEY = '56c754aa365a357c7242b15f23b7187ac749a6ec28e9f2775c49b498c5d42825'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: 30

ALLOWED_HOSTS = []

DATABASE = {
    "connections": {
        "default": "sqlite://db.sqlite3"
    },
    "apps": {
        "models": {
            "models": [
                "auth.models",
                "polls.models",
                "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}

STATIC_DIR = 'static'
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
