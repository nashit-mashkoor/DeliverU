from datetime import timedelta

from fastapi import HTTPException, status

from backend.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.database.crud import AsyncSessionLocal
from backend.database.models import User, UserRole
from backend.modules.auth.auth_dto import (
    AdminCreateUserRequest,
    ChangePasswordRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from backend.services.auth import AuthService
from backend.utils.exceptions import NotFoundError
from backend.utils.logging import Logging

logging_instance = Logging()
logger = logging_instance.get_logger()


class AuthenticationService:
    """Service for user authentication and management"""

    async def register_user(self, request: UserRegisterRequest) -> UserResponse:
        """Register a new user"""
        logger.info("Registering new user", extra={"email": request.email})

        try:
            user = await AuthService.create_user(
                email=request.email,
                password=request.password,
                role=UserRole.CUSTOMER,
            )
            logger.info("User registered successfully", extra={"user_id": user.id})

            return UserResponse(
                uuid=user.uuid,
                email=user.email,
                is_active=user.is_active,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )

        except ValueError as e:
            logger.error("Registration failed", extra={"email": request.email, "error": str(e)})
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.error("Registration error", extra={"email": request.email, "error": str(e)})
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register user")

    async def login_user(self, request: UserLoginRequest) -> TokenResponse:
        """Authenticate user and return JWT tokens"""
        logger.info("User login attempt", extra={"email": request.email})

        user = await AuthService.authenticate_user(email=request.email, password=request.password)

        if not user:
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

    async def get_current_user(self, user_id: int) -> UserResponse:
        """Get current user information"""
        async with AsyncSessionLocal() as session:
            user = await User.get_by_id(session, user_id)

            if not user:
                raise NotFoundError("User", user_id)

            return UserResponse(
                uuid=user.uuid,
                email=user.email,
                is_active=user.is_active,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )

    async def create_user_by_admin(self, request: AdminCreateUserRequest) -> UserResponse:
        """Create a non-customer user account from admin flow."""
        if request.role == UserRole.CUSTOMER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin account creation endpoint only supports admin and driver roles",
            )

        try:
            user = await AuthService.create_user(email=request.email, password=request.password, role=request.role)
            return UserResponse(
                uuid=user.uuid,
                email=user.email,
                is_active=user.is_active,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def change_password(self, user_id: int, request: ChangePasswordRequest) -> dict:
        """Change user password"""
        logger.info("Password change request", extra={"user_id": user_id})

        async with AsyncSessionLocal() as session:
            user = await User.get_by_id(session, user_id)

            if not user:
                raise NotFoundError("User", user_id)

            if not AuthService.verify_password(request.current_password, user.hashed_password):
                logger.warning("Password change failed - invalid current password", extra={"user_id": user_id})
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password is incorrect")

            new_hashed_password = AuthService.get_password_hash(request.new_password)
            await User.update_by_id(session, user_id, hashed_password=new_hashed_password)
            await session.commit()

            logger.info("Password changed successfully", extra={"user_id": user_id})
            return {"message": "Password changed successfully"}

    async def deactivate_user(self, user_id: int) -> dict:
        """Deactivate a user account"""
        logger.info("Deactivating user", extra={"user_id": user_id})

        async with AsyncSessionLocal() as session:
            user = await User.update_by_id(session, user_id, is_active=False)

            if not user:
                raise NotFoundError("User", user_id)

            await session.commit()
            logger.info("User deactivated", extra={"user_id": user_id})
            return {"message": "User account deactivated"}
