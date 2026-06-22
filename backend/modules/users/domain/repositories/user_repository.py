from abc import ABC, abstractmethod
from uuid import UUID

from backend.modules.users.domain.entities.user import User
from backend.modules.users.domain.value_objects.email import Email


class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> None:
        """Persist a new user."""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        """Return a user by identity, if one exists."""

    @abstractmethod
    async def get_by_email(self, email: Email) -> User | None:
        """Return a user by normalized email, if one exists."""
