from backend.modules.users.application.dto.register_user_request import RegisterUserRequest
from backend.modules.users.application.dto.register_user_response import RegisterUserResponse
from backend.modules.users.application.interfaces.password_hasher import PasswordHasher
from backend.modules.users.domain.entities.user import User
from backend.modules.users.domain.exceptions import UserAlreadyExistsError
from backend.modules.users.domain.repositories.user_repository import UserRepository
from backend.modules.users.domain.value_objects.email import Email
from backend.modules.users.domain.value_objects.password_hash import PasswordHash


class RegisterUserUseCase:
    """Use case for registering a new user.

    Constructor receives required dependencies via dependency injection.
    """

    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def execute(self, request: RegisterUserRequest) -> RegisterUserResponse:
        # Normalize email
        email = Email(request.email)

        # Check for existing user
        existing = await self._user_repository.get_by_email(email)
        if existing is not None:
            raise UserAlreadyExistsError(str(email))

        # Hash password
        hashed = await self._password_hasher.hash_password(request.password)

        # Create password hash value object
        password_hash = PasswordHash(hashed)

        # Create user entity
        user = User.create(email=email, display_name=request.display_name, password_hash=password_hash)

        # Persist user
        await self._user_repository.add(user)

        # Build and return response
        return RegisterUserResponse(id=user.id, email=user.email.value, display_name=user.display_name)
