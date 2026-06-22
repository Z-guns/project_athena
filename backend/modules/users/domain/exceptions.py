from uuid import UUID


class UserDomainError(Exception):
    """Base exception for user-domain rule violations."""


class InvalidEmailError(UserDomainError):
    def __init__(self, email: object) -> None:
        super().__init__(f"Invalid email address: {email!r}")


class InvalidDisplayNameError(UserDomainError):
    def __init__(self) -> None:
        super().__init__("Display name must contain between 1 and 100 characters")


class InvalidPasswordHashError(UserDomainError):
    def __init__(self) -> None:
        super().__init__("Password hash must be a valid encoded hash")


class UserAlreadyExistsError(UserDomainError):
    def __init__(self, email: str) -> None:
        super().__init__(f"A user with email {email!r} already exists")


class UserNotFoundError(UserDomainError):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(f"User {user_id} was not found")
