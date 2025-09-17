"""
Configuration Management for Rocket.net MCP Servers
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration for Rocket.net API access."""

    email: str
    password: str
    api_base: str = "https://control.rocket.net/api"
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds
    log_level: str = "INFO"
    timeout: int = 30  # seconds
    max_retries: int = 3
    retry_delay: int = 1  # seconds

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        email = os.getenv("ROCKETNET_EMAIL")
        password = os.getenv("ROCKETNET_PASSWORD")

        if not email or not password:
            raise ValueError(
                "ROCKETNET_EMAIL and ROCKETNET_PASSWORD environment variables are required. "
                "Please set them in your .env file or environment."
            )

        return cls(
            email=email,
            password=password,
            api_base=os.getenv("ROCKETNET_API_BASE", "https://control.rocket.net/api"),
            rate_limit_requests=int(os.getenv("ROCKETNET_RATE_LIMIT_REQUESTS", "100")),
            rate_limit_period=int(os.getenv("ROCKETNET_RATE_LIMIT_PERIOD", "60")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            timeout=int(os.getenv("ROCKETNET_TIMEOUT", "30")),
            max_retries=int(os.getenv("ROCKETNET_MAX_RETRIES", "3")),
            retry_delay=int(os.getenv("ROCKETNET_RETRY_DELAY", "1")),
        )

    def validate(self) -> bool:
        """Validate configuration values."""
        if not self.email or not self.password:
            return False

        if not self.api_base.startswith("http"):
            return False

        if self.rate_limit_requests <= 0 or self.rate_limit_period <= 0:
            return False

        return True