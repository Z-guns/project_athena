from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    display_name: str
    password: str
