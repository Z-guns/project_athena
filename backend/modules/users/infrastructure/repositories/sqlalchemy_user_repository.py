from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.users.domain.entities.user import User
from backend.modules.users.domain.repositories.user_repository import UserRepository
from backend.modules.users.domain.value_objects.email import Email
from backend.modules.users.domain.value_objects.password_hash import PasswordHash
from backend.modules.users.infrastructure.models.user import UserORM


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository for async operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user: User) -> None:
        """Persist a new user."""
        orm = self._to_orm(user)
        self._session.add(orm)

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Return a user by identity, if one exists."""
        stmt = select(UserORM).where(UserORM.id == user_id)
        result = await self._session.execute(stmt)
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm is not None else None

    async def get_by_email(self, email: Email) -> User | None:
        """Return a user by normalized email, if one exists."""
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self._session.execute(stmt)
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm is not None else None

    @staticmethod
    def _to_orm(user: User) -> UserORM:
        """Convert domain User aggregate to ORM persistence model."""
        return UserORM(
            id=user.id,
            email=user.email.value,
            password_hash=user.password_hash.value,
            display_name=user.display_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @staticmethod
    def _to_domain(orm: UserORM) -> User:
        """Convert ORM persistence model to domain User aggregate."""
        return User(
            id=orm.id,
            email=Email(orm.email),
            password_hash=PasswordHash(orm.password_hash),
            display_name=orm.display_name,
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
