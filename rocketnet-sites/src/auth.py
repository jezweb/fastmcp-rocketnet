"""
Simple Authentication for Rocket.net API
"""

import os
import logging
from typing import Optional, Dict, Any
import httpx

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Authentication failed error."""
    pass


async def login_to_rocketnet(
    username: Optional[str] = None,
    password: Optional[str] = None,
    api_base: str = "https://api.rocket.net/v1"
) -> str:
    """
    Login to Rocket.net and get a JWT token.

    Args:
        username: Rocket.net username (falls back to ROCKETNET_USERNAME env var)
        password: Rocket.net password (falls back to ROCKETNET_PASSWORD env var)
        api_base: API base URL

    Returns:
        JWT token string

    Raises:
        AuthenticationError: If login fails
        ValueError: If credentials are missing
    """
    # Get credentials from params or environment
    final_username = username or os.getenv("ROCKETNET_USERNAME") or os.getenv("ROCKETNET_EMAIL")
    final_password = password or os.getenv("ROCKETNET_PASSWORD")

    if not final_username or not final_password:
        raise ValueError(
            "Username and password required. "
            "Provide them as parameters or set ROCKETNET_USERNAME and ROCKETNET_PASSWORD environment variables."
        )

    # Login endpoint
    login_url = f"{api_base}/login"

    # Prepare request
    payload = {
        "username": final_username,
        "password": final_password
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            logger.debug(f"Attempting login for user: {final_username}")
            response = await client.post(
                login_url,
                json=payload,
                headers=headers
            )

            if response.status_code == 200:
                data = response.json()
                token = data.get("token")
                if not token:
                    raise AuthenticationError("No token in response")
                logger.info("Successfully authenticated with Rocket.net")
                return token
            elif response.status_code == 401:
                raise AuthenticationError("Invalid username or password")
            elif response.status_code == 400:
                raise AuthenticationError("Invalid request format")
            else:
                raise AuthenticationError(
                    f"Authentication failed with status {response.status_code}: {response.text}"
                )

    except httpx.RequestError as e:
        logger.error(f"Network error during authentication: {e}")
        raise AuthenticationError(f"Failed to connect to Rocket.net API: {str(e)}")


async def get_auth_headers(
    username: Optional[str] = None,
    password: Optional[str] = None,
    api_base: str = "https://api.rocket.net/v1"
) -> Dict[str, str]:
    """
    Get authorization headers for API requests.
    Automatically handles login to get token.

    Args:
        username: Rocket.net username (optional)
        password: Rocket.net password (optional)
        api_base: API base URL

    Returns:
        Dictionary with Authorization header
    """
    token = await login_to_rocketnet(username, password, api_base)
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


async def make_api_request(
    method: str,
    endpoint: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    json_data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    api_base: str = "https://api.rocket.net/v1"
) -> Dict[str, Any]:
    """
    Make an authenticated API request to Rocket.net.

    This is a simple helper that:
    1. Gets auth headers (handles login automatically)
    2. Makes the API request
    3. Returns the response

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        endpoint: API endpoint (e.g., "/sites" or "sites")
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)
        json_data: JSON body for POST/PUT requests
        params: Query parameters for GET requests
        api_base: Base API URL

    Returns:
        Response data as dictionary

    Raises:
        Exception: For API errors
        AuthenticationError: For auth failures
    """
    # Get auth headers (this handles login automatically)
    headers = await get_auth_headers(username, password, api_base)

    # Ensure endpoint starts with /
    if not endpoint.startswith("/"):
        endpoint = f"/{endpoint}"

    # Build full URL
    url = f"{api_base}{endpoint}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=json_data,
                params=params
            )

            # Handle response
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 201:
                return response.json()
            elif response.status_code == 204:
                return {"success": True, "message": "Operation completed"}
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code == 400:
                raise Exception(f"Bad request: {response.text}")
            elif response.status_code == 401:
                raise AuthenticationError("Authentication failed - invalid token")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                raise Exception(f"Unexpected response: {response.status_code} - {response.text}")

    except httpx.RequestError as e:
        logger.error(f"Network error: {e}")
        raise Exception(f"Network error: {str(e)}")