from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Self
from uuid import UUID, uuid4

from backend.modules.users.domain.exceptions import (
    InvalidDisplayNameError,
    UserDomainError,
)
from backend.modules.users.domain.value_objects.email import Email
from backend.modules.users.domain.value_objects.password_hash import PasswordHash


def _utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(eq=False, slots=True)
class User:
    id: UUID
    email: Email
    password_hash: PasswordHash
    display_name: str
    is_active: bool = True
    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        self.display_name = self._validate_display_name(self.display_name)

        if self.created_at.tzinfo is None or self.updated_at.tzinfo is None:
            raise UserDomainError("User timestamps must be timezone-aware")

        if self.updated_at < self.created_at:
            raise UserDomainError("User updated_at cannot precede created_at")

    @classmethod
    def create(
        cls,
        email: Email,
        display_name: str,
        password_hash: PasswordHash,
    ) -> Self:
        now = _utc_now()

        return cls(
            id=uuid4(),
            email=email,
            password_hash=password_hash,
            display_name=display_name,
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def _validate_display_name(value: str) -> str:
        normalized = value.strip()

        if not 1 <= len(normalized) <= 100:
            raise InvalidDisplayNameError

        return normalized

    def change_email(self, email: Email) -> None:
        if self.email == email:
            return

        self.email = email
        self.updated_at = _utc_now()

    def rename(self, display_name: str) -> None:
        normalized = self._validate_display_name(display_name)

        if self.display_name == normalized:
            return

        self.display_name = normalized
        self.updated_at = _utc_now()

    def activate(self) -> None:
        if self.is_active:
            return

        self.is_active = True
        self.updated_at = _utc_now()

    def deactivate(self) -> None:
        if not self.is_active:
            return

        self.is_active = False
        self.updated_at = _utc_now()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, User) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
  