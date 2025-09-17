"""
Rocket.net Performance & CDN MCP Server
========================================
CDN cache management, performance monitoring, and optimization.
"""

import os
import sys
from pathlib import Path

from fastmcp import FastMCP
from utils import format_success, format_error

# Import tools
from tools.performance import (
    purge_cache_files,
    purge_all_cache,
    get_cdn_requests_report,
    get_cache_status_report,
    get_cache_content_report,
    get_visitors_report,
    get_bandwidth_usage,
    get_top_bandwidth_consumers,
)

# Initialize FastMCP server - MUST be at module level for FastMCP Cloud
mcp = FastMCP(
    name="rocketnet-performance",
    instructions="""
    This server provides performance and CDN management tools for Rocket.net sites.

    Available tools:
    - purge_cache_files: Purge specific files from CDN cache
    - purge_all_cache: Clear entire CDN cache for a site
    - get_cdn_requests_report: View CDN request patterns and statistics
    - get_cache_status_report: Monitor cache hit rates and performance
    - get_cache_content_report: Analyze cached content by type
    - get_visitors_report: Get visitor analytics and geographic data
    - get_bandwidth_usage: Monitor bandwidth consumption
    - get_top_bandwidth_consumers: Identify high-bandwidth resources

    Performance Features:
    - Cloudflare CDN integration
    - Real-time cache management
    - Bandwidth optimization
    - Visitor analytics
    - Performance monitoring

    Resources:
    - performance://{site_id}/overview - Complete performance metrics
    - cache://{site_id}/status - Current cache status

    All operations require proper authentication via environment variables:
    ROCKETNET_EMAIL and ROCKETNET_PASSWORD
    """
)

# Register tools
mcp.tool(purge_cache_files)
mcp.tool(purge_all_cache)
mcp.tool(get_cdn_requests_report)
mcp.tool(get_cache_status_report)
mcp.tool(get_cache_content_report)
mcp.tool(get_visitors_report)
mcp.tool(get_bandwidth_usage)
mcp.tool(get_top_bandwidth_consumers)

# Register resources
@mcp.resource("performance://{site_id}/overview")
async def performance_overview_resource(site_id: str) -> str:
    """Get complete performance overview for a site."""
    try:
        from auth import make_api_request
        import json

        # Get multiple reports
        cdn_response = await make_api_request(
            "GET",
            f"/reporting/sites/{site_id}/cdn-requests",
            params={"period": "24h"}
        )

        bandwidth_response = await make_api_request(
            "GET",
            f"/reporting/sites/{site_id}/bandwidth/usage",
            params={"period": "30d"}
        )

        overview = {
            "site_id": site_id,
            "cdn_metrics": cdn_response.get("report", {}),
            "bandwidth_metrics": bandwidth_response.get("report", {}),
            "timestamp": "current"
        }

        return json.dumps(overview, indent=2)
    except Exception as e:
        import json
        return json.dumps({"error": str(e)}, indent=2)

@mcp.resource("cache://{site_id}/status")
async def cache_status_resource(site_id: str) -> str:
    """Get current cache status for a site."""
    try:
        from auth import make_api_request
        import json

        response = await make_api_request(
            "GET",
            f"/reporting/sites/{site_id}/cdn-cache-status",
            params={"period": "1h"}
        )

        return json.dumps({
            "site_id": site_id,
            "cache_status": response.get("report", response.get("data", {}))
        }, indent=2)
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