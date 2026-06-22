from enum import StrEnum
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Self

from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    Field,
    PostgresDsn,
    RedisDsn,
    SecretStr,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        env_prefix="ATHENA_",
        case_sensitive=False,
        extra="ignore",
        validate_default=True,
    )

    app_name: Annotated[str, Field(min_length=1, max_length=100)] = "Project Athena"
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = False
    log_level: LogLevel = LogLevel.INFO
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[AnyHttpUrl] = Field(default_factory=list)

    database_url: PostgresDsn
    redis_url: RedisDsn

    secret_key: SecretStr
    jwt_algorithm: Annotated[str, Field(pattern=r"^HS(256|384|512)$")] = "HS256"
    jwt_access_token_expire_minutes: Annotated[int, Field(gt=0, le=1440)] = 30

    openai_api_key: SecretStr | None = None
    gemini_api_key: SecretStr | None = None
    anthropic_api_key: SecretStr | None = None

    playwright_headless: bool = True
    vector_database_url: AnyUrl | None = None

    @field_validator("api_v1_prefix")
    @classmethod
    def validate_api_v1_prefix(cls, value: str) -> str:
        normalized = value.rstrip("/")
        if not normalized.startswith("/"):
            raise ValueError("API prefix must start with '/'")
        if normalized == "":
            raise ValueError("API prefix cannot be the root path")
        return normalized

    @field_validator(
        "openai_api_key",
        "gemini_api_key",
        "anthropic_api_key",
        "vector_database_url",
        mode="before",
    )
    @classmethod
    def empty_string_to_none(cls, value: object) -> object:
        return None if value == "" else value

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: SecretStr) -> SecretStr:
        if len(value.get_secret_value()) < 32:
            raise ValueError("Secret key must contain at least 32 characters")
        return value

    @model_validator(mode="after")
    def validate_production_settings(self) -> Self:
        if self.environment is Environment.PRODUCTION:
            if self.debug:
                raise ValueError("Debug mode must be disabled in production")
            if self.secret_key.get_secret_value() == "replace-with-a-secure-random-value":
                raise ValueError("Placeholder secret key cannot be used in production")
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
