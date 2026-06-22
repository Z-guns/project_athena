from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Abstract interface for asynchronous password hashing operations."""

    @abstractmethod
    async def hash_password(self, password: str) -> str:
        """
        Hash a password asynchronously.

        Args:
            password: The plaintext password to hash.

        Returns:
            The hashed password.
        """
        pass

    @abstractmethod
    async def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash asynchronously.

        Args:
            password: The plaintext password to verify.
            password_hash: The hashed password to verify against.

        Returns:
            True if the password matches the hash, False otherwise.
        """
        pass
