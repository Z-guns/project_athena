from dataclasses import dataclass

from backend.modules.users.domain.exceptions import InvalidPasswordHashError


@dataclass(frozen=True, slots=True, repr=False)
class PasswordHash:
    value: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.value, str)
            or not 32 <= len(self.value) <= 1024
            or self.value != self.value.strip()
            or any(character.isspace() for character in self.value)
        ):
            raise InvalidPasswordHashError

    def __repr__(self) -> str:
        return "PasswordHash(***)"

    def __str__(self) -> str:
        return "***"
