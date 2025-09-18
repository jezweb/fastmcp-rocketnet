"""
Rocket.net Analytics & Reporting MCP Server
============================================
Comprehensive reporting, logging, and security analytics.
"""

import os
import sys
from pathlib import Path

from fastmcp import FastMCP
from utils import format_success, format_error

# Import tools
from tools.analytics import (
    get_access_logs,
    get_waf_events,
    get_waf_events_by_source,
    get_firewall_events_timeline,
    get_request_volume_by_source,
    get_total_requests_report,
    get_account_visitors_overview,
    get_site_health_report,
)

# Initialize FastMCP server - MUST be at module level for FastMCP Cloud
mcp = FastMCP(
    name="rocketnet-analytics",
    instructions="""
    This server provides comprehensive analytics and reporting tools for Rocket.net sites.

    Available tools:
    - get_access_logs: Retrieve and analyze access logs
    - get_waf_events: View Web Application Firewall security events
    - get_waf_events_by_source: Analyze threats by source IP/country
    - get_firewall_events_timeline: Track security events over time
    - get_request_volume_by_source: Geographic request distribution
    - get_total_requests_report: Comprehensive request statistics
    - get_account_visitors_overview: Account-wide visitor analytics
    - get_site_health_report: Complete site health assessment

    Analytics Features:
    - Security monitoring (WAF, firewall events)
    - Access log analysis
    - Geographic analytics
    - Performance trending
    - Health scoring and recommendations
    - Account-wide reporting

    Resources:
    - analytics://{site_id}/health - Site health dashboard
    - security://{site_id}/overview - Security events overview

    All operations require proper authentication via environment variables:
    ROCKETNET_USERNAME and ROCKETNET_PASSWORD
    """
)

# Register tools
mcp.tool(get_access_logs)
mcp.tool(get_waf_events)
mcp.tool(get_waf_events_by_source)
mcp.tool(get_firewall_events_timeline)
mcp.tool(get_request_volume_by_source)
mcp.tool(get_total_requests_report)
mcp.tool(get_account_visitors_overview)
mcp.tool(get_site_health_report)

# Register resources
@mcp.resource("analytics://{site_id}/health")
async def site_health_resource(site_id: str) -> str:
    """Get complete health dashboard for a site."""
    try:
        from auth import make_api_request
        import json
        from datetime import datetime

        # Get various metrics
        perf_response = await make_api_request(
            "GET",
            f"/sites/{site_id}/reporting/total-requests",
            params={"period": "24h"}
        )

        waf_response = await make_api_request(
            "GET",
            f"/sites/{site_id}/reporting/waf-eventlist",
            params={"period": "24h"}
        )

        health_dashboard = {
            "site_id": site_id,
            "timestamp": datetime.now().isoformat(),
            "performance": perf_response.get("report", {}),
            "security_events": len(waf_response.get("events", [])),
            "status": "healthy"
        }

        return json.dumps(health_dashboard, indent=2)
    except Exception as e:
        import json
        return json.dumps({"error": str(e)}, indent=2)

@mcp.resource("security://{site_id}/overview")
async def security_overview_resource(site_id: str) -> str:
    """Get security events overview for a site."""
    try:
        from auth import make_api_request
        import json

        # Get WAF events
        waf_response = await make_api_request(
            "GET",
            f"/sites/{site_id}/reporting/waf-eventlist",
            params={"period": "24h"}
        )

        # Get events by source
        sources_response = await make_api_request(
            "GET",
            f"/sites/{site_id}/reporting/waf-events-source",
            params={"period": "24h"}
        )

        events = waf_response.get("events", [])
        sources = sources_response.get("sources", [])

        security_overview = {
            "site_id": site_id,
            "period": "24h",
            "total_events": len(events),
            "blocked_events": sum(1 for e in events if e.get("action") == "block"),
            "top_threat_sources": sources[:5] if sources else [],
            "threat_level": "low" if len(events) < 50 else "medium" if len(events) < 200 else "high"
        }

        return json.dumps(security_overview, indent=2)
    except Exception as e:
        import json
        return json.dumps({"error": str(e)}, indent=2)

# Optional: Local testing
if __name__ == "__main__":
    import asyncio
    import logging
    from dotenv import load_dotenv

    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    asyncio.run(mcp.run())