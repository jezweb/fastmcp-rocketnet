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