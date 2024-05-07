from fastapi import APIRouter

from src.api.controller import health, approvals_detector

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(
    approvals_detector.router, prefix="/approval-detection", tags=["approval-detection"]
)
