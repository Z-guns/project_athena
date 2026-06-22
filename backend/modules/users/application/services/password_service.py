from backend.modules.users.application.interfaces.password_hasher import PasswordHasher


class PasswordService:
    """Service for password hashing and verification operations."""

    def __init__(self, password_hasher: PasswordHasher) -> None:
        """Initialize the password service.

        Args:
            password_hasher: The password hasher implementation to use.
        """
        self._password_hasher = password_hasher

    async def hash(self, password: str) -> str:
        """Hash a password.

        Args:
            password: The plaintext password to hash.

        Returns:
            The hashed password.
        """
        return await self._password_hasher.hash_password(password)

    async def verify(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash.

        Args:
            password: The plaintext password to verify.
            password_hash: The hashed password to verify against.

        Returns:
            True if the password matches the hash, False otherwise.
        """
        return await self._password_hasher.verify_password(password, password_hash)
