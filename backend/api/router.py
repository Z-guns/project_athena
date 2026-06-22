from typing import Literal

from fastapi import APIRouter, status
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


health_router = APIRouter(tags=["health"])


@health_router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Check API health",
)
async def health_check() -> HealthResponse:
    return HealthResponse()


# The API version prefix is applied by create_app through Settings.api_v1_prefix.
api_router = APIRouter()
api_router.include_router(health_router)

# Future feature routers are registered below this line.
