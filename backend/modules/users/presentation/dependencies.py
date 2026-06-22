from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infrastructure.database import session_scope
from backend.modules.users.application.interfaces.password_hasher import PasswordHasher
from backend.modules.users.application.interfaces.user_unit_of_work import (
    UserUnitOfWork,
)
from backend.modules.users.infrastructure.security.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from backend.modules.users.infrastructure.unit_of_work.sqlalchemy_user_unit_of_work import (
    SQLAlchemyUserUnitOfWork,
)


async def get_db() -> AsyncIterator[AsyncSession]:
    """Yield an AsyncSession using the project's `session_scope()`.

    Presentation-only adapter that re-uses the centralized session context.
    """
    async with session_scope() as session:
        yield session


async def get_user_uow(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AsyncIterator[UserUnitOfWork]:
    """Yield a per-request `SQLAlchemyUserUnitOfWork` bound to the request session."""
    async with SQLAlchemyUserUnitOfWork(db) as uow:
        yield uow


def get_password_hasher() -> PasswordHasher:
    """Return the module's `PasswordHasher` implementation."""
    return BcryptPasswordHasher()
