from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.router import api_router
from backend.core.config import Settings, settings
from backend.core.logging import configure_logging


logger = structlog.get_logger(__name__)


def create_app(
    *,
    app_settings: Settings = settings,
) -> FastAPI:
    configure_logging(
        log_level=app_settings.log_level.value,
        environment=app_settings.environment.value,
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        await logger.ainfo(
            "application_started",
            environment=app_settings.environment.value,
        )
        try:
            yield
        finally:
            await logger.ainfo("application_stopped")

    application = FastAPI(
        title=app_settings.app_name,
        version="0.1.0",
        debug=app_settings.debug,
        lifespan=lifespan,
        docs_url="/docs" if app_settings.environment.value != "production" else None,
        redoc_url="/redoc" if app_settings.environment.value != "production" else None,
        openapi_url=(
            "/openapi.json" if app_settings.environment.value != "production" else None
        ),
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in app_settings.cors_origins],
        allow_credentials=bool(app_settings.cors_origins),
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
    application.include_router(api_router, prefix=app_settings.api_v1_prefix)

    return application
