import asyncio
from typing import Optional

from backend.modules.users.application.interfaces.password_hasher import PasswordHasher

# Prefer Argon2; fall back to bcrypt if Argon2 isn't available.
_ARGON2: Optional[object]
_BCRYPT: Optional[object]

try:
    # Try to use pwdlib's Argon2 if present
    from pwdlib.hash import argon2 as _pwdlib_argon2  # type: ignore

    _ARGON2 = _pwdlib_argon2
    _BCRYPT = None
except Exception:
    try:
        # Fallback to argon2-cffi
        from argon2 import PasswordHasher as _Argon2PasswordHasher  # type: ignore

        _ARGON2 = _Argon2PasswordHasher()
        _BCRYPT = None
    except Exception:
        try:
            import bcrypt as _bcrypt  # type: ignore

            _ARGON2 = None
            _BCRYPT = _bcrypt
        except Exception:
            _ARGON2 = None
            _BCRYPT = None


class BcryptPasswordHasher(PasswordHasher):
    """Password hasher using Argon2 (preferred) or bcrypt as a fallback.

    Async methods run blocking libraries in a thread pool.
    """

    async def hash_password(self, password: str) -> str:
        if _ARGON2 is not None:
            # pwdlib.argon2 exposes a callable API or argon2-cffi provides PasswordHasher
            if hasattr(_ARGON2, "hash"):
                return await asyncio.to_thread(_ARGON2.hash, password)
            # pwdlib.argon2 may expose a 'hash' function
            return await asyncio.to_thread(_ARGON2, password)  # type: ignore

        if _BCRYPT is not None:
            salt = await asyncio.to_thread(_BCRYPT.gensalt)
            hashed = await asyncio.to_thread(_BCRYPT.hashpw, password.encode("utf-8"), salt)
            return hashed.decode("utf-8")

        raise RuntimeError("No supported password backend is available")

    async def verify_password(self, password: str, password_hash: str) -> bool:
        if _ARGON2 is not None:
            # argon2-cffi PasswordHasher.verify(hash, password) may raise exceptions on mismatch
            try:
                if hasattr(_ARGON2, "verify"):
                    return await asyncio.to_thread(_ARGON2.verify, password_hash, password)
                # pwdlib.argon2 may provide a verify function
                return await asyncio.to_thread(_ARGON2.verify, password_hash, password)  # type: ignore
            except Exception:
                return False

        if _BCRYPT is not None:
            try:
                return await asyncio.to_thread(
                    _BCRYPT.checkpw, password.encode("utf-8"), password_hash.encode("utf-8")
                )
            except Exception:
                return False

        raise RuntimeError("No supported password backend is available")
