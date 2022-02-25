

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.settings import ALLOWED_HOSTS


def register_cors(app: FastAPI):
    origins = ALLOWED_HOSTS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
