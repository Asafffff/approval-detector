from fastapi import FastAPI

from src.api.router import api_router
from src.api.core.config import settings
from src.util.logger import setup_logger

setup_logger()
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/openapi.json",
)

app.include_router(api_router)
