from typing import Dict

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.session import get_db
from backend.modules.auth.auth_dto import (
    AdminCreateUserRequest,
    ChangePasswordRequest,
    RefreshTokenResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from backend.modules.auth.auth_service import AuthenticationService
from backend.services.security import JWTBearer, require_admin

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
auth_service = AuthenticationService()
security = JWTBearer()


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(request: UserRegisterRequest, session: AsyncSession = Depends(get_db)) -> UserResponse:
    """Register a new user account."""
    return await auth_service.register_user(session=session, request=request)


@auth_router.post("/login", response_model=TokenResponse)
async def login(request: UserLoginRequest, session: AsyncSession = Depends(get_db)) -> TokenResponse:
    """Authenticate user and receive access token and refresh token."""
    return await auth_service.login_user(session=session, request=request)


@auth_router.post("/refresh-token", response_model=RefreshTokenResponse)
async def refresh_token(
    authorization: str = Header(...),
    session: AsyncSession = Depends(get_db),
) -> RefreshTokenResponse:
    """Refresh access token using a refresh token."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format")

    refresh_token_value = authorization.replace("Bearer ", "", 1).strip()

    if not refresh_token_value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not provided")

    return await auth_service.refresh_access_token(session=session, refresh_token_value=refresh_token_value)


@auth_router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: dict = Depends(security),
    session: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Get current authenticated user information."""
    return await auth_service.get_current_user(session=session, user_id=current_user["user_id"])


@auth_router.post("/change-password", response_model=Dict[str, str])
async def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(security),
    session: AsyncSession = Depends(get_db),
) -> Dict[str, str]:
    """Change the current user's password."""
    return await auth_service.change_password(session=session, user_id=current_user["user_id"], request=request)


@auth_router.post("/logout", response_model=Dict[str, str])
async def logout(current_user: dict = Depends(security), session: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    """Logout the current user."""
    return await auth_service.logout_user(session=session, user_id=current_user["user_id"])


@auth_router.post("/deactivate", response_model=Dict[str, str])
async def deactivate_account(
    current_user: dict = Depends(security),
    session: AsyncSession = Depends(get_db),
) -> Dict[str, str]:
    """Deactivate the current user's account."""
    return await auth_service.deactivate_user(session=session, user_id=current_user["user_id"])


@auth_router.post("/admin/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_from_admin(
    request: AdminCreateUserRequest,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Create admin or driver users from an authenticated admin session."""
    return await auth_service.create_user_by_admin(session=session, request=request)
