from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.modules.users.presentation.dependencies import (
    get_password_hasher,
    get_user_uow,
)
from backend.modules.users.presentation.schemas import (
    RegisterUserRequestSchema,
    RegisterUserResponseSchema,
)
from backend.modules.users.application.commands.register_user_command import (
    RegisterUserCommand,
)
from backend.modules.users.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from backend.modules.users.application.interfaces.password_hasher import (
    PasswordHasher,
)
from backend.modules.users.application.interfaces.user_unit_of_work import (
    UserUnitOfWork,
)
from backend.modules.users.domain.exceptions import UserAlreadyExistsError


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=RegisterUserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description=(
        "Register a new user account. Returns the created user's id, email,"
        " and display name."
    ),
)
async def register_user(
    request: RegisterUserRequestSchema,
    uow: Annotated[UserUnitOfWork, Depends(get_user_uow)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> RegisterUserResponseSchema:
    """Thin endpoint for registering a new user.

    Maps the HTTP request to a `RegisterUserCommand`, invokes the
    `RegisterUserUseCase`, and returns a `RegisterUserResponseSchema`.
    """

    command = RegisterUserCommand(
        email=request.email,
        display_name=request.display_name,
        password=request.password,
    )

    use_case = RegisterUserUseCase(
        user_repository=uow.users, password_hasher=password_hasher, uow=uow
    )

    try:
        user = await use_case.execute(command)
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return RegisterUserResponseSchema(
        id=user.id, email=user.email.value, display_name=user.display_name
    )
