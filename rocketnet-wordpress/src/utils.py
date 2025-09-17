"""
Utility functions for formatting responses
"""

from typing import Any, Dict, Optional, List
from datetime import datetime


def format_success(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Format a successful response."""
    response = {
        "success": True,
        "message": message
    }
    if data:
        response["data"] = data
    return response


def format_error(message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Format an error response."""
    response = {
        "success": False,
        "error": message
    }
    if details:
        response["details"] = details
    return response


def format_warning(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Format a warning response."""
    response = {
        "success": True,
        "warning": message
    }
    if data:
        response["data"] = data
    return response


def format_datetime(dt_str: Optional[str]) -> Optional[str]:
    """Format datetime string for display."""
    if not dt_str:
        return None

    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return dt_str


def format_size(size_bytes: int) -> str:
    """Format bytes into human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def format_list(items: List[Any], key: Optional[str] = None) -> str:
    """Format a list of items for display."""
    if not items:
        return "None"

    if key:
        return ", ".join(str(item.get(key, '')) for item in items)
    return ", ".join(str(item) for item in items)