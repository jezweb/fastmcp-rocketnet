"""
Performance and CDN Management Tools for Rocket.net
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

# Add parent directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import make_api_request
from utils import format_success, format_error, format_warning, format_size


async def purge_cache_files(
    site_id: str,
    files: List[str],
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Purge specific files from the CDN cache.

    Args:
        site_id: The ID of the site
        files: List of file URLs or paths to purge
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the cache purge operation
    """
    try:
        payload = {
            "files": files
        }

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/cache/purge",
            json_data=payload,
            username=username,
            password=password
        )
        result = response.get("result", response.get("data", response))

        return format_success(
            f"Cache purge initiated for {len(files)} files",
            {
                "site_id": site_id,
                "purged_files": files,
                "count": len(files),
                "status": result.get("status", "success"),
                "purge_id": result.get("purge_id"),
                "message": "Files will be refreshed from origin on next request"
            }
        )

    except Exception as e:
        return format_error(f"Failed to purge cache files: {str(e)}")


async def purge_all_cache(
    site_id: str,
    confirm: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Purge all files from the site's CDN cache.

    Args:
        site_id: The ID of the site
        confirm: Must be True to confirm full cache purge
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the cache purge operation
    """
    try:
        if not confirm:
            return format_warning(
                "Full cache purge requires confirmation",
                {
                    "message": "Set confirm=True to purge entire cache. This may temporarily increase origin load.",
                    "site_id": site_id
                }
            )

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/cache/purge_everything",
            username=username,
            password=password
        )
        result = response.get("result", response.get("data", response))

        return format_success(
            f"Full cache purge initiated for site {site_id}",
            {
                "site_id": site_id,
                "status": result.get("status", "success"),
                "purge_id": result.get("purge_id"),
                "estimated_time": "2-5 minutes",
                "message": "All cached content will be refreshed from origin"
            }
        )

    except Exception as e:
        return format_error(f"Failed to purge all cache: {str(e)}")


async def get_cdn_requests_report(
    site_id: str,
    period: str = "24h",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get CDN requests report showing traffic patterns.

    Args:
        site_id: The ID of the site
        period: Time period (1h, 6h, 24h, 7d, 30d)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        CDN request statistics and patterns
    """
    try:
        params = {"period": period}

        response = await make_api_request(
            method="GET",
            endpoint=f"/reporting/sites/{site_id}/cdn-requests",
            params=params,
            username=username,
            password=password
        )
        report = response.get("report", response.get("data", response))

        return format_success(
            f"CDN requests report for site {site_id}",
            {
                "site_id": site_id,
                "period": period,
                "total_requests": report.get("total_requests"),
                "cached_requests": report.get("cached_requests"),
                "uncached_requests": report.get("uncached_requests"),
                "cache_hit_rate": f"{report.get('cache_hit_rate', 0)}%",
                "bandwidth_saved": format_size(report.get("bandwidth_saved", 0)),
                "top_requested_urls": report.get("top_requested_urls", [])[:5],
                "requests_by_status": {
                    "2xx": report.get("status_2xx", 0),
                    "3xx": report.get("status_3xx", 0),
                    "4xx": report.get("status_4xx", 0),
                    "5xx": report.get("status_5xx", 0)
                },
                "peak_hour": report.get("peak_hour"),
                "average_response_time": f"{report.get('average_response_time', 0)}ms"
            }
        )

    except Exception as e:
        return format_error(f"Failed to get CDN requests report: {str(e)}")


async def get_cache_status_report(
    site_id: str,
    period: str = "24h",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get CDN cache status report showing cache performance.

    Args:
        site_id: The ID of the site
        period: Time period (1h, 6h, 24h, 7d, 30d)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Cache status and performance metrics
    """
    try:
        params = {"period": period}

        response = await make_api_request(
            method="GET",
            endpoint=f"/reporting/sites/{site_id}/cdn-cache-status",
            params=params,
            username=username,
            password=password
        )
        report = response.get("report", response.get("data", response))

        return format_success(
            "CDN cache status report",
            {
                "site_id": site_id,
                "period": period,
                "cache_status": {
                    "hit": report.get("cache_hit", 0),
                    "miss": report.get("cache_miss", 0),
                    "bypass": report.get("cache_bypass", 0),
                    "expired": report.get("cache_expired", 0),
                    "stale": report.get("cache_stale", 0),
                    "updating": report.get("cache_updating", 0),
                    "revalidated": report.get("cache_revalidated", 0)
                },
                "hit_rate": f"{report.get('hit_rate', 0)}%",
                "byte_hit_rate": f"{report.get('byte_hit_rate', 0)}%",
                "origin_pulls": report.get("origin_pulls", 0),
                "cache_size": format_size(report.get("cache_size", 0)),
                "bandwidth_saved": format_size(report.get("bandwidth_saved", 0))
            }
        )

    except Exception as e:
        return format_error(f"Failed to get cache status report: {str(e)}")


async def get_cache_content_report(
    site_id: str,
    content_type: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get report of cached content by type.

    Args:
        site_id: The ID of the site
        content_type: Filter by content type (images, css, js, html, fonts)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Cached content breakdown and statistics
    """
    try:
        params = {}
        if content_type:
            params["content_type"] = content_type

        response = await make_api_request(
            method="GET",
            endpoint=f"/reporting/sites/{site_id}/cdn-cache-content",
            params=params,
            username=username,
            password=password
        )
        report = response.get("report", response.get("data", response))

        return format_success(
            "CDN cache content report",
            {
                "site_id": site_id,
                "content_type_filter": content_type,
                "content_breakdown": {
                    "images": {
                        "count": report.get("images_count", 0),
                        "size": format_size(report.get("images_size", 0)),
                        "hit_rate": f"{report.get('images_hit_rate', 0)}%"
                    },
                    "css": {
                        "count": report.get("css_count", 0),
                        "size": format_size(report.get("css_size", 0)),
                        "hit_rate": f"{report.get('css_hit_rate', 0)}%"
                    },
                    "javascript": {
                        "count": report.get("js_count", 0),
                        "size": format_size(report.get("js_size", 0)),
                        "hit_rate": f"{report.get('js_hit_rate', 0)}%"
                    },
                    "html": {
                        "count": report.get("html_count", 0),
                        "size": format_size(report.get("html_size", 0)),
                        "hit_rate": f"{report.get('html_hit_rate', 0)}%"
                    },
                    "fonts": {
                        "count": report.get("fonts_count", 0),
                        "size": format_size(report.get("fonts_size", 0)),
                        "hit_rate": f"{report.get('fonts_hit_rate', 0)}%"
                    },
                    "other": {
                        "count": report.get("other_count", 0),
                        "size": format_size(report.get("other_size", 0)),
                        "hit_rate": f"{report.get('other_hit_rate', 0)}%"
                    }
                },
                "total_cached_size": format_size(report.get("total_size", 0)),
                "total_cached_files": report.get("total_files", 0),
                "largest_files": report.get("largest_files", [])[:5]
            }
        )

    except Exception as e:
        return format_error(f"Failed to get cache content report: {str(e)}")


async def get_visitors_report(
    site_id: str,
    period: str = "24h",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get visitor statistics and geographic distribution.

    Args:
        site_id: The ID of the site
        period: Time period (1h, 6h, 24h, 7d, 30d)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Visitor analytics and patterns
    """
    try:
        params = {"period": period}

        response = await make_api_request(
            method="GET",
            endpoint=f"/reporting/sites/{site_id}/visitors",
            params=params,
            username=username,
            password=password
        )
        report = response.get("report", response.get("data", response))

        return format_success(
            f"Visitors report for site {site_id}",
            {
                "site_id": site_id,
                "period": period,
                "unique_visitors": report.get("unique_visitors"),
                "total_visits": report.get("total_visits"),
                "page_views": report.get("page_views"),
                "average_session_duration": f"{report.get('avg_session_duration', 0)} seconds",
                "bounce_rate": f"{report.get('bounce_rate', 0)}%",
                "top_countries": report.get("top_countries", [])[:5],
                "top_pages": report.get("top_pages", [])[:5],
                "top_referrers": report.get("top_referrers", [])[:5],
                "device_breakdown": {
                    "desktop": f"{report.get('desktop_percentage', 0)}%",
                    "mobile": f"{report.get('mobile_percentage', 0)}%",
                    "tablet": f"{report.get('tablet_percentage', 0)}%"
                },
                "browser_breakdown": report.get("browser_breakdown", {}),
                "new_vs_returning": {
                    "new": f"{report.get('new_visitors_percentage', 0)}%",
                    "returning": f"{report.get('returning_visitors_percentage', 0)}%"
                }
            }
        )

    except Exception as e:
        return format_error(f"Failed to get visitors report: {str(e)}")


async def get_bandwidth_usage(
    site_id: str,
    period: str = "30d",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get bandwidth usage statistics.

    Args:
        site_id: The ID of the site
        period: Time period (24h, 7d, 30d)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Bandwidth usage breakdown
    """
    try:
        params = {"period": period}

        response = await make_api_request(
            method="GET",
            endpoint=f"/reporting/sites/{site_id}/bandwidth/usage",
            params=params,
            username=username,
            password=password
        )
        report = response.get("report", response.get("data", response))

        return format_success(
            "Bandwidth usage report",
            {
                "site_id": site_id,
                "period": period,
                "total_bandwidth": format_size(report.get("total_bandwidth", 0)),
                "cdn_bandwidth": format_size(report.get("cdn_bandwidth", 0)),
                "origin_bandwidth": format_size(report.get("origin_bandwidth", 0)),
                "bandwidth_saved": format_size(report.get("bandwidth_saved", 0)),
                "savings_percentage": f"{report.get('savings_percentage', 0)}%",
                "daily_average": format_size(report.get("daily_average", 0)),
                "peak_day": {
                    "date": report.get("peak_date"),
                    "bandwidth": format_size(report.get("peak_bandwidth", 0))
                },
                "trend": report.get("trend", "stable"),
                "projected_monthly": format_size(report.get("projected_monthly", 0))
            }
        )

    except Exception as e:
        return format_error(f"Failed to get bandwidth usage: {str(e)}")


async def get_top_bandwidth_consumers(
    site_id: str,
    limit: int = 10,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get top bandwidth consuming resources.

    Args:
        site_id: The ID of the site
        limit: Number of top consumers to return
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of top bandwidth consuming resources
    """
    try:
        params = {"limit": limit}

        response = await make_api_request(
            method="GET",
            endpoint=f"/reporting/sites/{site_id}/bandwidth/top-usage",
            params=params,
            username=username,
            password=password
        )
        report = response.get("report", response.get("data", response))

        top_consumers = []
        for item in report.get("top_consumers", [])[:limit]:
            top_consumers.append({
                "url": item.get("url"),
                "bandwidth": format_size(item.get("bandwidth", 0)),
                "requests": item.get("requests"),
                "content_type": item.get("content_type"),
                "cache_status": item.get("cache_status"),
                "percentage_of_total": f"{item.get('percentage', 0)}%"
            })

        return format_success(
            f"Top {limit} bandwidth consumers",
            {
                "site_id": site_id,
                "top_consumers": top_consumers,
                "total_analyzed": report.get("total_analyzed"),
                "analysis_period": report.get("period", "30 days"),
                "optimization_suggestions": report.get("suggestions", [])
            }
        )

    except Exception as e:
        return format_error(f"Failed to get top bandwidth consumers: {str(e)}")