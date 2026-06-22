from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.users.application.interfaces.user_unit_of_work import UserUnitOfWork
from backend.modules.users.domain.repositories.user_repository import UserRepository
from backend.modules.users.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


class SQLAlchemyUserUnitOfWork(UserUnitOfWork):
    """SQLAlchemy-backed Unit of Work for user operations."""

    users: UserRepository

    def __init__(self, session: AsyncSession) -> None:
        """Create a unit of work bound to an AsyncSession."""
        self._session = session
        self.users = SQLAlchemyUserRepository(session)

    async def commit(self) -> None:
        """Persist pending changes."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Rollback pending changes."""
        await self._session.rollback()

    async def __aenter__(self) -> Self:
        """Enter the unit of work context."""
        return self

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        exc: BaseException | None,
        _tb: TracebackType | None,
    ) -> None:
        """Close the session and rollback on failure."""
        try:
            if exc is not None:
                await self.rollback()
        finally:
            await self._session.close()