from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserRegisterRequest(BaseModel):
    """Request model for user registration"""

    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str

    @validator("password_confirm")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("password")
    def password_strength(cls, v):
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
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class ChangePasswordRequest(BaseModel):
    """Request model for changing password"""

    current_password: str
    new_password: str = Field(..., min_length=8)
    new_password_confirm: str

    @validator("new_password_confirm")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("new_password")
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v

