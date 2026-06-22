import re
from dataclasses import dataclass

from backend.modules.users.domain.exceptions import InvalidEmailError


_LOCAL_PART_PATTERN = re.compile(r"^[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+$", re.IGNORECASE)
_DOMAIN_LABEL_PATTERN = re.compile(r"^[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?$", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", self._normalize(self.value))

    @staticmethod
    def _normalize(value: str) -> str:
        if not isinstance(value, str):
            raise InvalidEmailError(value)

        candidate = value.strip()
        if len(candidate) > 254 or candidate.count("@") != 1:
            raise InvalidEmailError(value)

        local_part, domain = candidate.rsplit("@", maxsplit=1)
        if not local_part or len(local_part) > 64 or any(char.isspace() for char in candidate):
            raise InvalidEmailError(value)
        if local_part.startswith(".") or local_part.endswith(".") or ".." in local_part:
            raise InvalidEmailError(value)
        if _LOCAL_PART_PATTERN.fullmatch(local_part) is None:
            raise InvalidEmailError(value)

        try:
            ascii_domain = domain.encode("idna").decode("ascii")
        except UnicodeError as error:
            raise InvalidEmailError(value) from error

        if len(ascii_domain) > 253:
            raise InvalidEmailError(value)
        labels = ascii_domain.split(".")
        if any(_DOMAIN_LABEL_PATTERN.fullmatch(label) is None for label in labels):
            raise InvalidEmailError(value)

        return f"{local_part.casefold()}@{ascii_domain.casefold()}"

    def __str__(self) -> str:
        return self.value
