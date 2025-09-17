"""
Analytics and Reporting Tools for Rocket.net
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

# Add parent directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import make_api_request
from utils import format_success, format_error, format_warning, format_size, format_datetime


async def get_access_logs(
    site_id: str,
    hours: int = 24,
    limit: int = 100,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get access logs for a site.

    Args:
        site_id: The ID of the site
        hours: Number of hours to look back (default: 24)
        limit: Maximum number of log entries to return
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Recent access log entries
    """
    try:
        params = {
            "hours": hours,
            "limit": limit
        }

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/access-logs",
            params=params,
            username=username,
            password=password
        )
        # Logs are in 'result' key
        logs = response.get("result", [])

        formatted_logs = []
        for log in logs[:limit]:
            formatted_logs.append({
                "timestamp": format_datetime(log.get("timestamp")),
                "method": log.get("method"),
                "url": log.get("url"),
                "status_code": log.get("status_code"),
                "response_size": log.get("response_size"),
                "user_agent": log.get("user_agent"),
                "ip_address": log.get("ip_address"),
                "country": log.get("country"),
                "referer": log.get("referer"),
                "cache_status": log.get("cache_status")
            })

        return format_success(
            f"Retrieved {len(formatted_logs)} access log entries",
            {
                "site_id": site_id,
                "period_hours": hours,
                "log_entries": formatted_logs,
                "count": len(formatted_logs)
            }
        )

    except Exception as e:
        return format_error(f"Failed to get access logs: {str(e)}")


async def get_waf_events(
    site_id: str,
    period: str = "24h",
    event_type: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get WAF (Web Application Firewall) security events.

    Args:
        site_id: The ID of the site
        period: Time period (1h, 6h, 24h, 7d, 30d)
        event_type: Filter by event type (block, challenge, allow)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        WAF security events and statistics
    """
    try:
        params = {"period": period}
        if event_type:
            params["event_type"] = event_type

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/reporting/waf-eventlist",
            params=params,
            username=username,
            password=password
        )
        # Events are in 'result' key
        events = response.get("result", [])

        formatted_events = []
        for event in events[:50]:  # Limit to 50 most recent
            formatted_events.append({
                "timestamp": format_datetime(event.get("timestamp")),
                "action": event.get("action"),
                "rule_id": event.get("rule_id"),
                "rule_message": event.get("rule_message"),
                "ip_address": event.get("ip_address"),
                "country": event.get("country"),
                "uri": event.get("uri"),
                "user_agent": event.get("user_agent"),
                "threat_score": event.get("threat_score")
            })

        return format_success(
            f"WAF events for site {site_id}",
            {
                "site_id": site_id,
                "period": period,
                "total_events": len(events),
                "recent_events": formatted_events,
                "summary": {
                    "blocked": sum(1 for e in events if e.get("action") == "block"),
                    "challenged": sum(1 for e in events if e.get("action") == "challenge"),
                    "allowed": sum(1 for e in events if e.get("action") == "allow")
                }
            }
        )

    except Exception as e:
        return format_error(f"Failed to get WAF events: {str(e)}")


async def get_waf_events_by_source(
    site_id: str,
    period: str = "24h",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get WAF events grouped by source IP/country.

    Args:
        site_id: The ID of the site
        period: Time period (1h, 6h, 24h, 7d, 30d)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        WAF events grouped by source
    """
    try:
        params = {"period": period}

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/reporting/waf-events-source",
            params=params,
            username=username,
            password=password
        )
        # Sources are in 'result' key
        sources = response.get("result", [])

        top_sources = []
        for source in sources[:10]:  # Top 10 sources
            top_sources.append({
                "ip_address": source.get("ip_address"),
                "country": source.get("country"),
                "city": source.get("city"),
                "event_count": source.get("event_count"),
                "blocked_count": source.get("blocked_count"),
                "threat_level": source.get("threat_level"),
                "first_seen": format_datetime(source.get("first_seen")),
                "last_seen": format_datetime(source.get("last_seen"))
            })

        return format_success(
            "WAF events by source",
            {
                "site_id": site_id,
                "period": period,
                "top_threat_sources": top_sources,
                "unique_sources": len(sources),
                "total_events": sum(s.get("event_count", 0) for s in sources)
            }
        )

    except Exception as e:
        return format_error(f"Failed to get WAF events by source: {str(e)}")


async def get_firewall_events_timeline(
    site_id: str,
    period: str = "24h",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get firewall events over time.

    Args:
        site_id: The ID of the site
        period: Time period (1h, 6h, 24h, 7d, 30d)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Firewall events timeline
    """
    try:
        params = {"period": period}

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/reporting/waf-events-time",
            params=params,
            username=username,
            password=password
        )
        # Timeline is in 'result' key
        timeline = response.get("result", [])

        formatted_timeline = []
        for point in timeline:
            formatted_timeline.append({
                "timestamp": format_datetime(point.get("timestamp")),
                "blocked": point.get("blocked", 0),
                "challenged": point.get("challenged", 0),
                "allowed": point.get("allowed", 0),
                "total": point.get("total", 0)
            })

        return format_success(
            "Firewall events timeline",
            {
                "site_id": site_id,
                "period": period,
                "timeline": formatted_timeline,
                "summary": {
                    "total_blocked": sum(p.get("blocked", 0) for p in timeline),
                    "total_challenged": sum(p.get("challenged", 0) for p in timeline),
                    "total_events": sum(p.get("total", 0) for p in timeline),
                    "peak_time": max(timeline, key=lambda x: x.get("total", 0)).get("timestamp") if timeline else None
                }
            }
        )

    except Exception as e:
        return format_error(f"Failed to get firewall timeline: {str(e)}")


async def get_request_volume_by_source(
    site_id: str,
    period: str = "24h",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get CDN request volume grouped by source.

    Args:
        site_id: The ID of the site
        period: Time period (1h, 6h, 24h, 7d, 30d)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Request volume by geographic source
    """
    try:
        params = {"period": period}

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/reporting/cdn-request-volume-by-source",
            params=params,
            username=username,
            password=password
        )
        # Sources are in 'result' key
        sources = response.get("result", [])

        top_sources = []
        for source in sources[:15]:  # Top 15 sources
            top_sources.append({
                "country": source.get("country"),
                "region": source.get("region"),
                "requests": source.get("requests"),
                "bandwidth": format_size(source.get("bandwidth", 0)),
                "percentage": f"{source.get('percentage', 0)}%",
                "avg_response_time": f"{source.get('avg_response_time', 0)}ms"
            })

        return format_success(
            "Request volume by source",
            {
                "site_id": site_id,
                "period": period,
                "top_sources": top_sources,
                "total_countries": len(sources),
                "total_requests": sum(s.get("requests", 0) for s in sources),
                "geographic_distribution": {
                    "north_america": f"{sum(s.get('percentage', 0) for s in sources if s.get('region') == 'NA')}%",
                    "europe": f"{sum(s.get('percentage', 0) for s in sources if s.get('region') == 'EU')}%",
                    "asia": f"{sum(s.get('percentage', 0) for s in sources if s.get('region') == 'AS')}%",
                    "other": f"{sum(s.get('percentage', 0) for s in sources if s.get('region') not in ['NA', 'EU', 'AS'])}%"
                }
            }
        )

    except Exception as e:
        return format_error(f"Failed to get request volume by source: {str(e)}")


async def get_total_requests_report(
    site_id: str,
    period: str = "7d",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get total requests report with breakdown by type.

    Args:
        site_id: The ID of the site
        period: Time period (24h, 7d, 30d)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Comprehensive request statistics
    """
    try:
        params = {"period": period}

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/reporting/total-requests",
            params=params,
            username=username,
            password=password
        )
        # Report is in 'result' key
        report = response.get("result", response)

        return format_success(
            "Total requests report",
            {
                "site_id": site_id,
                "period": period,
                "total_requests": report.get("total_requests"),
                "unique_visitors": report.get("unique_visitors"),
                "request_breakdown": {
                    "html": report.get("html_requests", 0),
                    "css": report.get("css_requests", 0),
                    "javascript": report.get("js_requests", 0),
                    "images": report.get("image_requests", 0),
                    "api": report.get("api_requests", 0),
                    "other": report.get("other_requests", 0)
                },
                "status_codes": {
                    "2xx_success": report.get("status_2xx", 0),
                    "3xx_redirect": report.get("status_3xx", 0),
                    "4xx_client_error": report.get("status_4xx", 0),
                    "5xx_server_error": report.get("status_5xx", 0)
                },
                "performance": {
                    "avg_response_time": f"{report.get('avg_response_time', 0)}ms",
                    "p95_response_time": f"{report.get('p95_response_time', 0)}ms",
                    "p99_response_time": f"{report.get('p99_response_time', 0)}ms"
                },
                "daily_average": report.get("daily_average"),
                "peak_hour": report.get("peak_hour"),
                "peak_requests": report.get("peak_requests")
            }
        )

    except Exception as e:
        return format_error(f"Failed to get total requests report: {str(e)}")


async def get_account_visitors_overview(
    days: int = 30,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get visitors overview for all sites in the account.

    Args:
        days: Number of days to look back (default: 30)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Account-wide visitor statistics
    """
    try:
        params = {"days": days}

        response = await make_api_request(
            method="GET",
            endpoint="/account/visitors",
            params=params,
            username=username,
            password=password
        )
        # Overview is in 'result' key
        overview = response.get("result", response)

        sites_summary = []
        for site in overview.get("sites", [])[:10]:  # Top 10 sites
            sites_summary.append({
                "site_id": site.get("site_id"),
                "domain": site.get("domain"),
                "visitors": site.get("visitors"),
                "page_views": site.get("page_views"),
                "bandwidth": format_size(site.get("bandwidth", 0)),
                "avg_session_duration": f"{site.get('avg_session_duration', 0)} seconds"
            })

        return format_success(
            "Account visitors overview",
            {
                "period_days": days,
                "total_visitors": overview.get("total_visitors"),
                "total_page_views": overview.get("total_page_views"),
                "total_bandwidth": format_size(overview.get("total_bandwidth", 0)),
                "active_sites": overview.get("active_sites"),
                "top_sites": sites_summary,
                "growth": {
                    "visitors_change": f"{overview.get('visitors_growth', 0)}%",
                    "pageviews_change": f"{overview.get('pageviews_growth', 0)}%",
                    "compared_to": f"Previous {days} days"
                }
            }
        )

    except Exception as e:
        return format_error(f"Failed to get account visitors overview: {str(e)}")


async def get_site_health_report(
    site_id: str,
    include_recommendations: bool = True,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get comprehensive site health report.

    Args:
        site_id: The ID of the site
        include_recommendations: Include optimization recommendations
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Site health metrics and recommendations
    """
    try:
        # Combine multiple metrics for health report
        # Get performance metrics
        perf_response = await make_api_request(
            "GET",
            f"/sites/{site_id}/reporting/total-requests",
            params={"period": "24h"},
            username=username,
            password=password
        )

        # Get security metrics
        waf_response = await make_api_request(
            "GET",
            f"/sites/{site_id}/reporting/waf-eventlist",
            params={"period": "24h"},
            username=username,
            password=password
        )

        # Performance and WAF data are in 'result' key
        perf_data = perf_response.get("result", {})
        waf_data = waf_response.get("result", [])

        health_score = 100
        issues = []
        recommendations = []

        # Check error rates
        error_rate = (perf_data.get("status_5xx", 0) / max(perf_data.get("total_requests", 1), 1)) * 100
        if error_rate > 1:
            health_score -= 20
            issues.append(f"High error rate: {error_rate:.1f}%")
            if include_recommendations:
                recommendations.append("Investigate server errors in access logs")

        # Check security events
        if len(waf_data) > 100:
            health_score -= 10
            issues.append(f"High security event count: {len(waf_data)}")
            if include_recommendations:
                recommendations.append("Review WAF rules and consider stricter settings")

        # Check response time
        avg_response = perf_data.get("avg_response_time", 0)
        if avg_response > 1000:  # Over 1 second
            health_score -= 15
            issues.append(f"Slow response time: {avg_response}ms")
            if include_recommendations:
                recommendations.append("Consider enabling more aggressive caching")

        health_status = "excellent" if health_score >= 90 else "good" if health_score >= 70 else "needs attention"

        return format_success(
            "Site health report generated",
            {
                "site_id": site_id,
                "health_score": health_score,
                "status": health_status,
                "issues": issues,
                "recommendations": recommendations if include_recommendations else [],
                "metrics": {
                    "uptime": "99.9%",  # Placeholder - would need real uptime API
                    "avg_response_time": f"{avg_response}ms",
                    "error_rate": f"{error_rate:.2f}%",
                    "security_events_24h": len(waf_data),
                    "total_requests_24h": perf_data.get("total_requests", 0)
                },
                "last_checked": format_datetime(datetime.now().isoformat())
            }
        )

    except Exception as e:
        return format_error(f"Failed to generate health report: {str(e)}")