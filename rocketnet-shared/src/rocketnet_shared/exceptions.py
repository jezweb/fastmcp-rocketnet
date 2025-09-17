"""
Custom Exceptions for Rocket.net API Operations
"""


class RocketnetAPIError(Exception):
    """Base exception for Rocket.net API errors."""

    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class AuthenticationError(RocketnetAPIError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class RateLimitError(RocketnetAPIError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class NotFoundError(RocketnetAPIError):
    """Raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ValidationError(RocketnetAPIError):
    """Raised when request validation fails."""

    def __init__(self, message: str = "Validation failed", errors: dict = None):
        super().__init__(message, status_code=400)
        self.errors = errors or {}


class ServerError(RocketnetAPIError):
    """Raised when server returns 5xx error."""

    def __init__(self, message: str = "Server error", status_code: int = 500):
        super().__init__(message, status_code=status_code)