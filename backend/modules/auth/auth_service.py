from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.database.models import User, UserRole
from backend.modules.auth.auth_dto import (
    AdminCreateUserRequest,
    ChangePasswordRequest,
    RefreshTokenResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from backend.modules.auth.auth_repository import AuthRepository
from backend.services.security import AuthService
from backend.utils.exceptions import NotFoundError
from backend.utils.logging import Logging

logging_instance = Logging()
logger = logging_instance.get_logger()


class AuthenticationService:
    """Service for user authentication and management"""

    @staticmethod
    def _build_user_response(user: User) -> UserResponse:
        return UserResponse(
            uuid=user.uuid,
            email=user.email,
            is_active=user.is_active,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def register_user(self, session: AsyncSession, request: UserRegisterRequest) -> UserResponse:
        """Register a new user"""
        logger.info("Registering new user", extra={"email": request.email})

        try:
            existing_user = await AuthRepository.get_user_by_email(session, request.email)
            if existing_user:
                raise ValueError(f"User with email {request.email} already exists")

            user = await AuthRepository.create_user(
                session,
                email=request.email,
                hashed_password=AuthService.get_password_hash(request.password),
                role=UserRole.CUSTOMER,
            )
            await session.commit()
            await session.refresh(user)
            logger.info("User registered successfully", extra={"user_id": user.id})

            return self._build_user_response(user)

        except ValueError as e:
            logger.error("Registration failed", extra={"email": request.email, "error": str(e)})
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.error("Registration error", extra={"email": request.email, "error": str(e)})
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register user")

    async def login_user(self, session: AsyncSession, request: UserLoginRequest) -> TokenResponse:
        """Authenticate user and return JWT tokens"""
        logger.info("User login attempt", extra={"email": request.email})

        user = await AuthRepository.get_user_by_email(session, request.email)
        if not user or not AuthService.verify_password(request.password, user.hashed_password):
            logger.warning("Login failed - invalid credentials", extra={"email": request.email})
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        if not user.is_active:
            logger.warning("Login failed - inactive user", extra={"email": request.email})
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is inactive")

        token_data = {
            "sub": user.email,
            "user_id": user.id,
            "user_uuid": user.uuid,
            "role": AuthService.get_role_value(user.role),
        }

        access_token = AuthService.create_access_token(
            data=token_data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = AuthService.create_refresh_token(data=token_data)

        logger.info("User logged in successfully", extra={"user_id": user.id})

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def refresh_access_token(self, session: AsyncSession, refresh_token_value: str) -> RefreshTokenResponse:
        """Refresh an access token using a valid refresh token."""
        try:
            payload = AuthService.decode_token(refresh_token_value)
            subject = payload.get("sub")

            if not isinstance(subject, str) or not subject:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

            if payload.get("token_type") != "refresh":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token type")

            user = await AuthRepository.get_user_by_email(session, subject)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            if not user.is_active:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is inactive")

            if AuthService.is_token_invalidated(payload, user):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token has been invalidated. Please login again.",
                )

            access_token = AuthService.create_access_token(
                data={
                    "sub": subject,
                    "user_id": payload.get("user_id"),
                    "user_uuid": payload.get("user_uuid"),
                    "role": payload.get("role"),
                }
            )

            logger.info("Token refreshed successfully", extra={"user_id": payload.get("user_id")})
            return RefreshTokenResponse(access_token=access_token, token_type="bearer")
        except ExpiredSignatureError:
            logger.warning("Refresh token expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired. Please login again.",
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid refresh token: {str(e)}")

    async def get_current_user(self, session: AsyncSession, user_id: int) -> UserResponse:
        """Get current user information"""
        user = await AuthRepository.get_user_by_id(session, user_id)

        if not user:
            raise NotFoundError("User", user_id)

        return self._build_user_response(user)

    async def create_user_by_admin(self, session: AsyncSession, request: AdminCreateUserRequest) -> UserResponse:
        """Create a non-customer user account from admin flow."""
        if request.role == UserRole.CUSTOMER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin account creation endpoint only supports admin and driver roles",
            )

        try:
            existing_user = await AuthRepository.get_user_by_email(session, request.email)
            if existing_user:
                raise ValueError(f"User with email {request.email} already exists")

            user = await AuthRepository.create_user(
                session,
                email=request.email,
                hashed_password=AuthService.get_password_hash(request.password),
                role=request.role,
            )
            await session.commit()
            await session.refresh(user)
            return self._build_user_response(user)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def change_password(self, session: AsyncSession, user_id: int, request: ChangePasswordRequest) -> dict:
        """Change user password"""
        logger.info("Password change request", extra={"user_id": user_id})

        user = await AuthRepository.get_user_by_id(session, user_id)

        if not user:
            raise NotFoundError("User", user_id)

        if not AuthService.verify_password(request.current_password, user.hashed_password):
            logger.warning("Password change failed - invalid current password", extra={"user_id": user_id})
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password is incorrect")

        new_hashed_password = AuthService.get_password_hash(request.new_password)
        await AuthRepository.update_password(session, user, new_hashed_password)
        await session.commit()

        logger.info("Password changed successfully", extra={"user_id": user_id})
        return {"message": "Password changed successfully"}

    async def logout_user(self, session: AsyncSession, user_id: int) -> dict:
        """Logout user by invalidating existing tokens."""
        logger.info("Logout request", extra={"user_id": user_id})
        user = await AuthRepository.get_user_by_id(session, user_id)
        if user:
            await AuthRepository.touch_user_updated_at(session, user, datetime.utcnow() + timedelta(seconds=1))
            await session.commit()
        return {"message": "Logged out successfully"}

    async def deactivate_user(self, session: AsyncSession, user_id: int) -> dict:
        """Deactivate a user account"""
        logger.info("Deactivating user", extra={"user_id": user_id})

        user = await AuthRepository.get_user_by_id(session, user_id)

        if not user:
            raise NotFoundError("User", user_id)

        await AuthRepository.deactivate_user(session, user)
        await session.commit()
        logger.info("User deactivated", extra={"user_id": user_id})
        return {"message": "User account deactivated"}
