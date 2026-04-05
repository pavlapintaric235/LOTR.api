import logging

from fastapi import FastAPI

from app.api import characters, hello
from app.db import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(hello.router)
    application.include_router(
        characters.router, prefix="/characters", tags=["characters"]
    )

    return application


app = create_application()

init_db(app)
