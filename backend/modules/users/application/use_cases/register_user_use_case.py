from backend.modules.users.application.commands.register_user_command import (
    RegisterUserCommand,
)
from backend.modules.users.application.interfaces.password_hasher import (
    PasswordHasher,
)
from backend.modules.users.application.interfaces.user_unit_of_work import (
    UserUnitOfWork,
)
from backend.modules.users.domain.entities.user import User
from backend.modules.users.domain.exceptions import UserAlreadyExistsError
from backend.modules.users.domain.repositories.user_repository import UserRepository
from backend.modules.users.domain.value_objects.email import Email
from backend.modules.users.domain.value_objects.password_hash import PasswordHash


class RegisterUserUseCase:
    """Application use case responsible for registering a new user."""

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        uow: UserUnitOfWork,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._uow = uow

    async def execute(self, command: RegisterUserCommand) -> User:
        email = Email(command.email)

        existing_user = await self._user_repository.get_by_email(email)
        if existing_user is not None:
            raise UserAlreadyExistsError(email.value)

        hashed_password = await self._password_hasher.hash_password(
            command.password
        )

        password_hash = PasswordHash(hashed_password)

        user = User.create(
            email=email,
            display_name=command.display_name,
            password_hash=password_hash,
        )

        await self._user_repository.add(user)
        await self._uow.commit()

        return user