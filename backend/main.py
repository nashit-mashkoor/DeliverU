import secrets
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator, Dict

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from backend.constants import API_PASSWORD, API_USER, FRONTEND_URL, PRODUCTION
from backend.modules.auth.auth_controller import auth_router
from backend.modules.items.item_controller import item_router
from backend.redis_engine import redis_close, redis_ping
from backend.utils.logging import Logging
from backend.utils.middlewares import LogRequestsMiddleware

logging_instance = Logging()
logger = logging_instance.get_logger()

# Security for API documentation
security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    """Verify credentials for API documentation access"""
    if not credentials.username or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is missing",
            headers={"WWW-Authenticate": "Basic"},
        )

    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")
    correct_username_bytes = API_USER.encode("utf8")
    correct_password_bytes = API_PASSWORD.encode("utf8")

    is_correct_username = secrets.compare_digest(current_username_bytes, correct_username_bytes)
    is_correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown tasks"""
    # Startup
    logger.info("Starting MyApp Backend")
    if await redis_ping():
        logger.info("Redis connection established")
    else:
        logger.warning("Redis connection failed - background tasks may not work")

    yield

    # Shutdown
    logger.info("Shutting down MyApp Backend")
    try:
        await redis_close()
    except Exception as e:
        logger.error(f"Error closing Redis: {e}")


# Create FastAPI app
app = FastAPI(
    title="MyApp API",
    description="A full-stack platform template API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)) -> HTMLResponse:
    """Serve Swagger UI documentation"""
    return get_swagger_ui_html(openapi_url="/openapi.json", title="MyApp API Docs")


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(get_current_username)) -> HTMLResponse:
    """Serve ReDoc documentation"""
    return get_redoc_html(openapi_url="/openapi.json", title="MyApp API Docs")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)) -> Dict:
    """Serve OpenAPI schema"""
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    redis_connected = await redis_ping()

    if not redis_connected:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "redis": "disconnected"}
        )

    return {"status": "healthy", "redis": "connected"}


# Build allowed origins list
allowed_origins = [FRONTEND_URL]
if not PRODUCTION:
    # Allow localhost variants in development
    allowed_origins.extend([
        "http://localhost:8503",
        "http://127.0.0.1:8503",
    ])

# Add CORS middleware with specific methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With",
        "X-Request-ID",
    ],
    expose_headers=["X-Request-ID"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

# Add trusted host middleware in production
if PRODUCTION:
    from urllib.parse import urlparse
    frontend_host = urlparse(FRONTEND_URL).hostname
    allowed_hosts = [frontend_host] if frontend_host else ["*"]
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Add request logging middleware
app.add_middleware(LogRequestsMiddleware)

# Include routers
app.include_router(auth_router)
app.include_router(item_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler - logs error but doesn't expose details"""
    logger.error(
        "Unhandled exception",
        extra={
            "path": request.url.path,
            "method": request.method,
            "error_type": type(exc).__name__,
            # Only log full error in non-production
            "error": str(exc) if not PRODUCTION else "redacted",
        }
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
