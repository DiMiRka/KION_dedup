from fastapi import APIRouter

from api.v1.events import events_router

api_router = APIRouter()

api_router.include_router(events_router)
