from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class RegisterUserResponse:
    """Response DTO for user registration."""

    id: UUID
    email: str
    display_name: str
