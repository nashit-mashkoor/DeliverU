from typing import Any, Dict, Optional


class BaseError(Exception):
    """Base exception class"""

    def __init__(self, message: str = "An error occurred", details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(BaseError):
    """Raised when a requested resource is not found"""

    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} with identifier {identifier} not found",
            details={"resource": resource, "identifier": identifier}
        )


class ValidationError(BaseError):
    """Raised when validation fails"""

    def __init__(self, field: str, message: str):
        super().__init__(
            message=f"Validation failed for field '{field}': {message}",
            details={"field": field, "validation_error": message}
        )


class AuthenticationError(BaseError):
    """Raised when authentication fails"""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message)


class AuthorizationError(BaseError):
    """Raised when authorization fails"""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message)

