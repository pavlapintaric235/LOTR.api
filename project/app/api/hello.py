from fastapi import APIRouter, Depends

from app.config import Settings, get_settings

router = APIRouter()


@router.get("/hello")
async def hello(settings: Settings = Depends(get_settings)):
    return {
        "message": "hello!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
