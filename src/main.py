from fastapi import FastAPI
import uvicorn

from core.config import uvicorn_options
from src.api import api_router

app = FastAPI(docs_url="/api/openapi")

app.include_router(api_router)

if __name__ == '__main__':
    print(uvicorn_options)
    uvicorn.run(
        'main:src',
        **uvicorn_options
    )
