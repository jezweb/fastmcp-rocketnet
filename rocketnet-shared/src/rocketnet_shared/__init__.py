"""
Rocket.net Shared Utilities Package
====================================
Common authentication, client, and utility functions for all Rocket.net MCP servers.
"""

from .auth import login_to_rocketnet, get_auth_headers
from .client import RocketnetClient, make_api_request
from .config import Config
from .exceptions import RocketnetAPIError, AuthenticationError, RateLimitError
from .utils import format_success, format_error, format_warning, parse_api_response

__all__ = [
    "login_to_rocketnet",
    "get_auth_headers",
    "make_api_request",
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