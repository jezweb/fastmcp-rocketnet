"""
Simple Authentication for Rocket.net API
"""

import os
import logging
from typing import Optional, Dict, Any
import httpx

from .exceptions import AuthenticationError

logger = logging.getLogger(__name__)


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