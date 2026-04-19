from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.constants import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY, REFRESH_TOKEN_EXPIRE_DAYS
from backend.database.crud import AsyncSessionLocal
from backend.database.models import User, UserRole
from backend.utils.exceptions import AuthenticationError
from backend.utils.logging import Logging

logging_instance = Logging()
logger = logging_instance.get_logger()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for authentication and authorization"""

    @staticmethod
    def _prepare_password(password: str) -> str:
        """Prepare password for bcrypt hashing (72-byte limit)"""
        password_bytes = password.encode("utf-8")
        if len(password_bytes) >= 72:
            password_bytes = password_bytes[:72]
        return password_bytes.decode("utf-8", errors="ignore")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        prepared_password = AuthService._prepare_password(plain_password)
        return pwd_context.verify(prepared_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        prepared_password = AuthService._prepare_password(password)
        return pwd_context.hash(prepared_password)

    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_role_value(role: UserRole | str) -> str:
        if isinstance(role, UserRole):
            return role.value
        return role

    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create a JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """Decode and validate a JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except JWTError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")

    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password"""
        async with AsyncSessionLocal() as session:
            users = await User.filter(session, email=email)
            if not users:
                return None

            user = users[0]
            if not AuthService.verify_password(password, user.hashed_password):
                return None

            return user

    @staticmethod
    async def create_user(email: str, password: str, role: UserRole = UserRole.CUSTOMER) -> User:
        """Create a new user"""
        hashed_password = AuthService.get_password_hash(password)

        async with AsyncSessionLocal() as session:
            existing_users = await User.filter(session, email=email)
            if existing_users:
                raise ValueError(f"User with email {email} already exists")

            user = await User.create(session, email=email, hashed_password=hashed_password, role=role)
            await session.commit()
            await session.refresh(user)

            logger.info(f"Created new user: {email}")
            return user


class JWTBearer(HTTPBearer):
    """JWT Bearer authentication dependency"""

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Dict[str, Any]:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")

            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")

            async with AsyncSessionLocal() as session:
                users = await User.filter(session, email=payload.get("sub"))
                if not users:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

                user = users[0]
                if not user.is_active:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

                return {
                    "user_id": user.id,
                    "email": user.email,
                    "role": AuthService.get_role_value(user.role),
                }
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = AuthService.decode_token(token)
            return payload
        except Exception as e:
            logger.error(f"JWT verification failed: {e}")
            return None


def require_admin(current_user: Dict[str, Any] = Depends(JWTBearer())) -> Dict[str, Any]:
    """Allow access only to admin users."""
    if current_user.get("role") != UserRole.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


def require_customer(current_user: Dict[str, Any] = Depends(JWTBearer())) -> Dict[str, Any]:
    """Allow access only to customer users."""
    if current_user.get("role") != UserRole.CUSTOMER.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Customer access required")
    return current_user


def require_driver(current_user: Dict[str, Any] = Depends(JWTBearer())) -> Dict[str, Any]:
    """Allow access only to driver users."""
    if current_user.get("role") != UserRole.DRIVER.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Driver access required")
    return current_user
