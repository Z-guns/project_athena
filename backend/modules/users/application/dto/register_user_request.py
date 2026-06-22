from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RegisterUserRequest:
    """Data transfer object for user registration requests."""
    email: str
    password: str
    display_name: str
