"""
Authentication Handler for Rocket.net API
"""

import time
import logging
from typing import Optional, Dict, Any
import httpx

from .config import Config
from .exceptions import AuthenticationError, RocketnetAPIError

logger = logging.getLogger(__name__)


class RocketnetAuth:
    """Handles authentication with Rocket.net API."""

    def __init__(self, config: Config):
        self.config = config
        self._token: Optional[str] = None
        self._token_expiry: Optional[float] = None
        self._refresh_token: Optional[str] = None

    @property
    def token(self) -> str:
        """Get current authentication token, refreshing if needed."""
        if not self._token or self._is_token_expired():
            self.authenticate()
        return self._token

    def _is_token_expired(self) -> bool:
        """Check if the current token has expired."""
        if not self._token_expiry:
            return True
        # Refresh token 5 minutes before expiry
        return time.time() > (self._token_expiry - 300)

    async def authenticate(self) -> str:
        """Authenticate with Rocket.net API and get JWT token."""
        auth_url = f"{self.config.api_base}/authentication/login"

        payload = {
            "email": self.config.email,
            "password": self.config.password
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    auth_url,
                    json=payload,
                    headers=headers,
                    timeout=self.config.timeout
                )

                if response.status_code == 200:
                    data = response.json()
                    self._token = data.get("token")
                    # Assume token is valid for 24 hours if not specified
                    self._token_expiry = time.time() + data.get("expires_in", 86400)
                    self._refresh_token = data.get("refresh_token")

                    logger.info("Successfully authenticated with Rocket.net API")
                    return self._token

                elif response.status_code == 401:
                    raise AuthenticationError(
                        "Invalid credentials. Please check your email and password."
                    )
                else:
                    raise AuthenticationError(
                        f"Authentication failed with status {response.status_code}: {response.text}"
                    )

        except httpx.RequestError as e:
            raise RocketnetAPIError(f"Failed to connect to Rocket.net API: {str(e)}")

    async def refresh_auth(self) -> str:
        """Refresh authentication token using refresh token."""
        if not self._refresh_token:
            # If no refresh token, do full authentication
            return await self.authenticate()

        refresh_url = f"{self.config.api_base}/authentication/refresh"

        payload = {
            "refresh_token": self._refresh_token
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    refresh_url,
                    json=payload,
                    headers=headers,
                    timeout=self.config.timeout
                )

                if response.status_code == 200:
                    data = response.json()
                    self._token = data.get("token")
                    self._token_expiry = time.time() + data.get("expires_in", 86400)

                    logger.info("Successfully refreshed authentication token")
                    return self._token
                else:
                    # Refresh failed, do full authentication
                    return await self.authenticate()

        except httpx.RequestError:
            # If refresh fails, fall back to full authentication
            return await self.authenticate()

    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token for API requests."""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def invalidate(self):
        """Invalidate current token."""
        self._token = None
        self._token_expiry = None
        logger.info("Authentication token invalidated")