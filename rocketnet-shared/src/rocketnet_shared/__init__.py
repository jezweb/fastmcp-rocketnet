"""
Rocket.net Shared Utilities Package
====================================
Common authentication, client, and utility functions for all Rocket.net MCP servers.
"""

from .auth import RocketnetAuth
from .client import RocketnetClient
from .config import Config
from .exceptions import RocketnetAPIError, AuthenticationError, RateLimitError
from .utils import format_success, format_error, format_warning, parse_api_response

__all__ = [
    "RocketnetAuth",
    "RocketnetClient",
    "Config",
    "RocketnetAPIError",
    "AuthenticationError",
    "RateLimitError",
    "format_success",
    "format_error",
    "format_warning",
    "parse_api_response",
]

__version__ = "1.0.0"