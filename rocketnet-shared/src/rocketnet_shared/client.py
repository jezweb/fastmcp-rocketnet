"""
HTTP Client Wrapper for Rocket.net API
"""

import asyncio
import time
import logging
from typing import Optional, Dict, Any, Union
import httpx
from urllib.parse import urljoin

from .auth import get_auth_headers
from .config import Config
from .exceptions import (
    RocketnetAPIError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ServerError,
)

logger = logging.getLogger(__name__)


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
        RocketnetAPIError: For API errors
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
                raise NotFoundError(f"Resource not found: {endpoint}")
            elif response.status_code == 400:
                raise ValidationError(f"Bad request: {response.text}")
            elif response.status_code == 401:
                raise RocketnetAPIError("Authentication failed - invalid token")
            elif response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            elif response.status_code >= 500:
                raise ServerError(f"Server error: {response.status_code}")
            else:
                raise RocketnetAPIError(f"Unexpected response: {response.status_code} - {response.text}")

    except httpx.RequestError as e:
        logger.error(f"Network error: {e}")
        raise RocketnetAPIError(f"Network error: {str(e)}")


class RocketnetClient:
    """HTTP client with authentication, retry logic, and rate limiting."""

    def __init__(self, config: Config):
        self.config = config
        self.auth = RocketnetAuth(config)
        self._request_times = []
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    async def _ensure_client(self):
        """Ensure HTTP client is initialized."""
        if not self._client:
            self._client = httpx.AsyncClient(timeout=self.config.timeout)

    async def _rate_limit(self):
        """Implement rate limiting."""
        now = time.time()
        # Remove old request times
        self._request_times = [
            t for t in self._request_times
            if now - t < self.config.rate_limit_period
        ]

        # Check if we've hit the rate limit
        if len(self._request_times) >= self.config.rate_limit_requests:
            # Calculate how long to wait
            oldest_request = self._request_times[0]
            wait_time = self.config.rate_limit_period - (now - oldest_request)
            if wait_time > 0:
                logger.warning(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
                await asyncio.sleep(wait_time)
                # Clear old requests after waiting
                self._request_times = []

        # Record this request
        self._request_times.append(now)

    async def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and errors."""
        if response.status_code == 200:
            try:
                return response.json()
            except Exception:
                return {"success": True, "data": response.text}

        elif response.status_code == 201:
            return response.json()

        elif response.status_code == 204:
            return {"success": True, "message": "Operation completed successfully"}

        elif response.status_code == 401:
            # Try to re-authenticate once
            await self.auth.authenticate()
            raise RocketnetAPIError("Authentication failed. Please check credentials.", 401)

        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {response.url}")

        elif response.status_code == 400:
            try:
                error_data = response.json()
                raise ValidationError(
                    message=error_data.get("message", "Validation failed"),
                    errors=error_data.get("errors", {})
                )
            except Exception:
                raise ValidationError(f"Bad request: {response.text}")

        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitError(
                f"Rate limit exceeded. Retry after {retry_after} seconds",
                retry_after=retry_after
            )

        elif response.status_code >= 500:
            raise ServerError(
                f"Server error ({response.status_code}): {response.text}",
                status_code=response.status_code
            )

        else:
            raise RocketnetAPIError(
                f"Unexpected response ({response.status_code}): {response.text}",
                status_code=response.status_code
            )

    async def request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Make an authenticated API request with retry logic."""
        await self._ensure_client()
        await self._rate_limit()

        # Ensure endpoint starts with /
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        url = urljoin(self.config.api_base, endpoint)

        # Get auth headers
        await self.auth.authenticate()  # Ensure we have a valid token
        headers = self.auth.get_headers()

        try:
            response = await self._client.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                params=params
            )

            return await self._handle_response(response)

        except RateLimitError as e:
            if retry_count < self.config.max_retries:
                wait_time = e.retry_after or self.config.retry_delay * (2 ** retry_count)
                logger.warning(f"Rate limited. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                return await self.request(
                    method, endpoint, json_data, params, retry_count + 1
                )
            raise

        except ServerError as e:
            if retry_count < self.config.max_retries:
                wait_time = self.config.retry_delay * (2 ** retry_count)
                logger.warning(f"Server error. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                return await self.request(
                    method, endpoint, json_data, params, retry_count + 1
                )
            raise

        except httpx.RequestError as e:
            if retry_count < self.config.max_retries:
                wait_time = self.config.retry_delay * (2 ** retry_count)
                logger.warning(f"Request failed: {e}. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                return await self.request(
                    method, endpoint, json_data, params, retry_count + 1
                )
            raise RocketnetAPIError(f"Request failed after {retry_count} retries: {str(e)}")

    # Convenience methods
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return await self.request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request."""
        return await self.request("POST", endpoint, json_data=json_data)

    async def put(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request."""
        return await self.request("PUT", endpoint, json_data=json_data)

    async def patch(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PATCH request."""
        return await self.request("PATCH", endpoint, json_data=json_data)

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        return await self.request("DELETE", endpoint)