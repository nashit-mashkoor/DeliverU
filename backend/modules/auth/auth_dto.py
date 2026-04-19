from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

from backend.database.models import UserRole


class UserRegisterRequest(BaseModel):
    """Request model for user registration"""

    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str

    @field_validator("password_confirm")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        password = info.data.get("password")
        if password and v != password:
            raise ValueError("Passwords do not match")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v


class UserLoginRequest(BaseModel):
    """Request model for user login"""

    email: EmailStr
    password: str


class AdminCreateUserRequest(BaseModel):
    """Request model for admin-created user accounts."""

    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v


class TokenResponse(BaseModel):
    """Response model for authentication tokens"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenResponse(BaseModel):
    """Response model for refreshed access token"""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Response model for user information"""

    uuid: str
    email: EmailStr
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime


class ChangePasswordRequest(BaseModel):
    """Request model for changing password"""

    current_password: str
    new_password: str = Field(..., min_length=8)
    new_password_confirm: str

    @field_validator("new_password_confirm")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        new_password = info.data.get("new_password")
        if new_password and v != new_password:
            raise ValueError("Passwords do not match")
        return v

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v
