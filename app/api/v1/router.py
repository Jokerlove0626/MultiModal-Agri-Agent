from fastapi import APIRouter
from app.api.v1.endpoints import health, diagnosis

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(diagnosis.router, prefix="/diagnosis", tags=["diagnosis"])
