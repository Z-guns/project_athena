from backend.modules.users.domain.entities.user import User
from backend.modules.users.domain.value_objects.email import Email
from backend.modules.users.domain.value_objects.password_hash import PasswordHash
from backend.modules.users.domain.repositories.user_repository import UserRepository
from backend.modules.users.domain.exceptions import UserAlreadyExistsError
from backend.modules.users.application.services.password_service import PasswordService
from backend.modules.users.application.dto.register_user_request import RegisterUserRequest
from backend.modules.users.application.dto.register_user_response import RegisterUserResponse


class RegisterUserUseCase:
    """Use case for registering a new user."""

    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
    ) -> None:
        """Initialize the register user use case.

        Args:
            user_repository: Repository for persisting users.
            password_service: Service for hashing passwords.
        """
        self._user_repository = user_repository
        self._password_service = password_service

    async def execute(
        self,
        request: RegisterUserRequest,
    ) -> RegisterUserResponse:
        """Execute user registration.

        Args:
            request: RegisterUserRequest containing email, password, and display_name.

        Returns:
            RegisterUserResponse with user_id, email, and display_name.

        Raises:
            InvalidEmailError: If email format is invalid.
            UserAlreadyExistsError: If email already exists.
            InvalidDisplayNameError: If display_name is invalid.
        """
        # 1. Create Email value object
        email = Email(request.email)

        # 2. Check email uniqueness
        existing_user = await self._user_repository.get_by_email(email)
        if existing_user is not None:
            raise UserAlreadyExistsError(email.value)

        # 3. Hash password
        hashed_password = await self._password_service.hash(request.password)

        # 4. Create PasswordHash value object
        password_hash = PasswordHash(hashed_password)

        # 5. Create User aggregate
        user = User.create(
            email=email,
            password_hash=password_hash,
            display_name=request.display_name,
        )

        # 6. Persist User
        await self._user_repository.add(user)

        # 7. Return RegisterUserResponse
        return RegisterUserResponse(
            user_id=user.id,
            email=user.email.value,
            display_name=user.display_name,
        )
