"""
HTTP Client Wrapper for Rocket.net API
"""

import asyncio
import time
import logging
from typing import Optional, Dict, Any, Union
import httpx
from urllib.parse import urljoin

from .auth import RocketnetAuth
from .config import Config
from .exceptions import (
    RocketnetAPIError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ServerError,
)

logger = logging.getLogger(__name__)


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