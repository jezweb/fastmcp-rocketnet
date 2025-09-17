"""
Utility Functions for Rocket.net MCP Servers
"""

import json
from typing import Dict, Any, Optional, List, Union
from datetime import datetime


def format_success(message: str, data: Optional[Any] = None) -> Dict[str, Any]:
    """Format a success response."""
    response = {
        "status": "success",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response


def format_error(message: str, details: Optional[Any] = None) -> Dict[str, Any]:
    """Format an error response."""
    response = {
        "status": "error",
        "message": message
    }
    if details is not None:
        response["details"] = details
    return response


def format_warning(message: str, data: Optional[Any] = None) -> Dict[str, Any]:
    """Format a warning response."""
    response = {
        "status": "warning",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response


def format_datetime(dt: Optional[Union[str, datetime]]) -> Optional[str]:
    """Format datetime to ISO string."""
    if dt is None:
        return None
    if isinstance(dt, str):
        return dt
    return dt.isoformat()


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def format_site_info(site: Dict[str, Any]) -> Dict[str, Any]:
    """Format site information for consistent output."""
    return {
        "id": site.get("id"),
        "name": site.get("name"),
        "domain": site.get("domain", site.get("primary_domain")),
        "status": site.get("status", "unknown"),
        "plan": site.get("plan", site.get("hosting_plan")),
        "location": site.get("location", site.get("datacenter")),
        "created_at": format_datetime(site.get("created_at")),
        "wordpress_version": site.get("wordpress_version"),
        "php_version": site.get("php_version"),
        "ssl_enabled": site.get("ssl_enabled", True),
        "backups_enabled": site.get("backups_enabled", True),
        "cdn_enabled": site.get("cdn_enabled", True)
    }