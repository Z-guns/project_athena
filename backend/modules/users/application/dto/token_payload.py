from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class TokenPayload:
    """Immutable DTO representing JWT token payload."""
    user_id: UUID
    email: str
