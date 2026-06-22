from abc import ABC, abstractmethod

from backend.modules.users.application.dto.token_payload import TokenPayload


class JwtProvider(ABC):
    """Abstract interface for JWT token operations."""

    @abstractmethod
    async def create_access_token(
        self,
        payload: TokenPayload,
    ) -> str:
        """Create an access token.

        Args:
            payload: The token payload containing user information.

        Returns:
            The access token string.
        """

    @abstractmethod
    async def verify_access_token(
        self,
        token: str,
    ) -> TokenPayload:
        """Verify an access token and extract the payload.

        Args:
            token: The access token to verify.

        Returns:
            The decoded token payload.
        """
