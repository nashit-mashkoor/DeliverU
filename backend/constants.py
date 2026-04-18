import os
import secrets
import sys
from dotenv import find_dotenv, load_dotenv

# Don't override environment variables that are already set
env_file = os.environ.get("ENV_FILE", ".env")
if os.path.isabs(env_file):
    env_path = env_file
else:
    env_path = find_dotenv(env_file, usecwd=True) or env_file
load_dotenv(env_path, override=False)


def strtobool(val: str) -> bool:
    """Convert a string representation of truth to bool."""
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truth value {val!r}")


# =============================================================================
# Environment Mode
# =============================================================================
PRODUCTION = strtobool(os.environ.get("PRODUCTION", "false"))


# =============================================================================
# Helper for environment-aware config
# =============================================================================
def get_secret(key: str, dev_default: str | None = None) -> str:
    """
    Get a secret from environment.
    - In development: auto-generates secure default if not set
    - In production: fails fast if not set
    """
    value = os.environ.get(key)
    
    if value:
        return value
    
    if PRODUCTION:
        raise RuntimeError(f"Required secret '{key}' is not set. Set it in your environment or .env file.")
    
    # Development: generate or use default
    if dev_default is None:
        generated = secrets.token_urlsafe(32)
        print(f"[DEV] Auto-generated {key}={generated}", file=sys.stderr)
        return generated
    
    return dev_default


# =============================================================================
# Database Configuration
# =============================================================================
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://root:password@pgbouncer:6432/deliveru"
)

# =============================================================================
# Authentication
# =============================================================================
JWT_SECRET_KEY = get_secret("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "120"))

# =============================================================================
# Redis Configuration
# =============================================================================
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")

# Build Redis URL with optional password
if REDIS_PASSWORD:
    REDIS_URL = os.environ.get("REDIS_URL", f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}")
else:
    REDIS_URL = os.environ.get("REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}")

# =============================================================================
# MinIO Configuration
# =============================================================================
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET_NAME = os.environ.get("MINIO_BUCKET_NAME", "uploads")
MINIO_SECURE = strtobool(os.environ.get("MINIO_SECURE", "false"))

# =============================================================================
# File Processing
# =============================================================================
MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", str(1024 * 1024 * 50)))  # 50MB

# =============================================================================
# Application URLs
# =============================================================================
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:8503")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8504")

# =============================================================================
# API Documentation Credentials
# =============================================================================
API_USER = os.environ.get("API_USER", "admin")
API_PASSWORD = get_secret("API_PASSWORD", "password" if not PRODUCTION else None)
