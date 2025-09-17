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


def parse_api_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Parse and standardize API response."""
    # Check if response already has our standard format
    if "status" in response:
        return response

    # Check for common success patterns
    if response.get("success") is True:
        return format_success(
            response.get("message", "Operation completed successfully"),
            response.get("data", response)
        )

    # Check for common error patterns
    if response.get("error") or response.get("errors"):
        return format_error(
            response.get("message", "Operation failed"),
            response.get("error") or response.get("errors")
        )

    # Default to success with the response as data
    return format_success("Operation completed", response)


def format_datetime(dt: Optional[Union[str, datetime]]) -> Optional[str]:
    """Format datetime to ISO string."""
    if dt is None:
        return None
    if isinstance(dt, str):
        return dt
    return dt.isoformat()


def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    """Parse ISO datetime string."""
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except Exception:
        return None


def safe_get(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Safely get nested dictionary value using dot notation."""
    keys = path.split('.')
    result = data

    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
            if result is None:
                return default
        else:
            return default

    return result


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split a list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


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


def validate_domain(domain: str) -> bool:
    """Validate domain name format."""
    import re
    # Basic domain validation
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))


def validate_email(email: str) -> bool:
    """Validate email address format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))