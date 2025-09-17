"""
Authentication module for Rocket.net API
Handles login and token management
"""

import os
from typing import Optional, Dict, Any
import httpx


async def login_to_rocketnet(
    username: Optional[str] = None,
    password: Optional[str] = None,
    api_base: str = "https://api.rocket.net/v1"
) -> str:
    """
    Login to Rocket.net API and get authentication token.

    Args:
        username: Rocket.net username/email (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)
        api_base: API base URL

    Returns:
        Authentication token
    """
    # Get credentials from params or environment
    final_username = username or os.getenv("ROCKETNET_USERNAME") or os.getenv("ROCKETNET_EMAIL")
    final_password = password or os.getenv("ROCKETNET_PASSWORD")

    if not final_username or not final_password:
        raise ValueError(
            "Rocket.net credentials required. Provide username/password parameters "
            "or set ROCKETNET_EMAIL/ROCKETNET_USERNAME and ROCKETNET_PASSWORD environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{api_base}/login",
            json={
                "username": final_username,
                "password": final_password
            }
        )
        response.raise_for_status()
        data = response.json()

        # Extract token from response
        token = data.get("token") or data.get("access_token")
        if not token:
            raise ValueError("No token received from Rocket.net API")

        return token


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

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, PATCH)
        endpoint: API endpoint (e.g., "/sites")
        username: Optional username for authentication
        password: Optional password for authentication
        json_data: Optional JSON data for request body
        params: Optional query parameters
        api_base: API base URL

    Returns:
        API response as dictionary
    """
    # Get token (fresh for each request)
    token = await login_to_rocketnet(username, password, api_base)

    # Make the API request
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Build full URL
        url = f"{api_base}{endpoint}" if endpoint.startswith("/") else f"{api_base}/{endpoint}"

        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            json=json_data,
            params=params,
            timeout=30.0
        )

        response.raise_for_status()
        return response.json()