from fastapi import APIRouter, Depends, HTTPException

events_router = APIRouter(prefix="/events", tags=['events'])


@events_router.post("/path")
def post_event():
    pass
