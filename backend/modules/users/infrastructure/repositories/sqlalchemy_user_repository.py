from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.users.domain.entities.user import User
from backend.modules.users.domain.repositories.user_repository import UserRepository
from backend.modules.users.domain.value_objects.email import Email
from backend.modules.users.domain.value_objects.password_hash import PasswordHash
from backend.modules.users.infrastructure.models.user import UserORM


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user: User) -> None:
        orm = UserORM(
            id=user.id,
            email=user.email.value,
            password_hash=user.password_hash.value,
            display_name=user.display_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        self._session.add(orm)

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(UserORM).where(UserORM.id == user_id)
        result = await self._session.execute(stmt)
        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        return self._to_domain(orm)

    async def get_by_email(self, email: Email) -> User | None:
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self._session.execute(stmt)
        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        return self._to_domain(orm)

    def _to_domain(self, orm: UserORM) -> User:
        return User(
            id=orm.id,
            email=Email(orm.email),
            password_hash=PasswordHash(orm.password_hash),
            display_name=orm.display_name,
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )