import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import characters, hello
from app.db import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(hello.router)
    application.include_router(
        characters.router, prefix="/characters", tags=["characters"]
    )

    return application


app = create_application()

init_db(app)
