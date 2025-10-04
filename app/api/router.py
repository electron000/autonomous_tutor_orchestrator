from fastapi import APIRouter
from.endpoints import orchestrator

api_router = APIRouter()
api_router.include_router(orchestrator.router, prefix="/v1", tags=["Orchestrator"])