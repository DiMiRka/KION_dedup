from fastapi import APIRouter

from src.api.v1.events import events_router

api_router = APIRouter()

api_router.include_router(events_router)
