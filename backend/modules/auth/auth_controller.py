from typing import Dict

from fastapi import APIRouter, Depends, Header, HTTPException, status
from jose import ExpiredSignatureError

from backend.modules.auth.auth_dto import (
    AdminCreateUserRequest,
    ChangePasswordRequest,
    RefreshTokenResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from backend.database.crud import AsyncSessionLocal
from backend.database.models import User
from backend.modules.auth.auth_service import AuthenticationService
from backend.services.auth import AuthService, JWTBearer, require_admin
from backend.utils.logging import Logging

logging_instance = Logging()
logger = logging_instance.get_logger()

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
auth_service = AuthenticationService()
security = JWTBearer()


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(request: UserRegisterRequest) -> UserResponse:
    """Register a new user account."""
    return await auth_service.register_user(request)


@auth_router.post("/login", response_model=TokenResponse)
async def login(request: UserLoginRequest) -> TokenResponse:
    """Authenticate user and receive access token and refresh token."""
    return await auth_service.login_user(request)


@auth_router.post("/refresh-token", response_model=RefreshTokenResponse)
async def refresh_token(authorization: str = Header(...)) -> RefreshTokenResponse:
    """Refresh access token using a refresh token."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format")

    refresh_token_value = authorization.replace("Bearer ", "", 1).strip()

    if not refresh_token_value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not provided")

    try:
        payload = AuthService.decode_token(refresh_token_value)

        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        if payload.get("token_type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token type")

        async with AsyncSessionLocal() as session:
            users = await User.filter(session, email=payload.get("sub"))
            if not users:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            user = users[0]
            if not user.is_active:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is inactive")

            if AuthService.is_token_invalidated(payload, user):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token has been invalidated. Please login again.",
                )

        access_token = AuthService.create_access_token(
            data={
                "sub": payload.get("sub"),
                "user_id": payload.get("user_id"),
                "user_uuid": payload.get("user_uuid"),
                "role": payload.get("role"),
            }
        )

        logger.info("Token refreshed successfully", extra={"user_id": payload.get("user_id")})
        return RefreshTokenResponse(access_token=access_token, token_type="bearer")

    except ExpiredSignatureError:
        logger.warning("Refresh token expired")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired. Please login again.")
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid refresh token: {str(e)}")


@auth_router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: dict = Depends(security)) -> UserResponse:
    """Get current authenticated user information."""
    return await auth_service.get_current_user(current_user["user_id"])


@auth_router.post("/change-password", response_model=Dict[str, str])
async def change_password(request: ChangePasswordRequest, current_user: dict = Depends(security)) -> Dict[str, str]:
    """Change the current user's password."""
    return await auth_service.change_password(user_id=current_user["user_id"], request=request)


@auth_router.post("/logout", response_model=Dict[str, str])
async def logout(current_user: dict = Depends(security)) -> Dict[str, str]:
    """Logout the current user."""
    logger.info("User logged out", extra={"user_id": current_user["user_id"]})
    return await auth_service.logout_user(current_user["user_id"])


@auth_router.post("/deactivate", response_model=Dict[str, str])
async def deactivate_account(current_user: dict = Depends(security)) -> Dict[str, str]:
    """Deactivate the current user's account."""
    return await auth_service.deactivate_user(current_user["user_id"])


@auth_router.post("/admin/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_from_admin(
    request: AdminCreateUserRequest,
    _: dict = Depends(require_admin),
) -> UserResponse:
    """Create admin or driver users from an authenticated admin session."""
    return await auth_service.create_user_by_admin(request)
