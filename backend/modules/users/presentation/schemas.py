from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterUserRequestSchema(BaseModel):
    email: EmailStr
    display_name: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class RegisterUserResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
    display_name: str

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
