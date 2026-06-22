from abc import ABC, abstractmethod
from typing import Self
from types import TracebackType

from backend.modules.users.domain.repositories.user_repository import UserRepository


class UserUnitOfWork(ABC):
    """Abstract unit-of-work for user-related operations."""

    users: UserRepository

    @abstractmethod
    async def commit(self) -> None:
        """Persist pending changes."""
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback pending changes."""
        ...

    @abstractmethod
    async def __aenter__(self) -> Self:
        ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        ...
