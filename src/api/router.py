from fastapi import APIRouter

from src.api.controller import approvals, health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["approvals"])
