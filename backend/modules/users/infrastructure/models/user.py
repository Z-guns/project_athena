from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String, UUID as SAUUIDType, text
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.database.base import Base


class UserORM(Base):
    """SQLAlchemy persistence model for users."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        SAUUIDType,
        primary_key=True,
    )

    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )