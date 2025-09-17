"""
Rocket.net Sites Management MCP Server
=======================================
Core site operations including creation, configuration, and monitoring.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastmcp import FastMCP
from rocketnet_shared import Config, RocketnetClient, format_success, format_error

# Import tools
from tools.sites import (
    list_sites,
    get_site,
    create_site,
    update_site,
    delete_site,
    get_site_status,
    clone_site,
    get_site_settings,
    update_site_settings,
)

from tools.locations import (
    list_locations,
    get_location_info,
)

from tools.plans import (
    list_plans,
    get_plan_details,
    change_site_plan,
)

# Import resources
from resources.dashboards import (
    get_site_dashboard,
    get_all_sites_status,
)

# Initialize FastMCP server - MUST be at module level for FastMCP Cloud
mcp = FastMCP(
    name="rocketnet-sites",
    instructions="""
    This server provides tools for managing Rocket.net sites.

    Available tools:
    - list_sites: Get all sites in your account
    - get_site: Get detailed information about a specific site
    - create_site: Create a new WordPress site
    - update_site: Update site configuration
    - delete_site: Delete a site (use with caution)
    - get_site_status: Check site health and status
    - clone_site: Create a copy of an existing site
    - get_site_settings: Get site settings
    - update_site_settings: Update site settings
    - list_locations: Get available data center locations
    - list_plans: Get available hosting plans
    - change_site_plan: Upgrade or downgrade a site's plan

    Resources:
    - site://{site_id}/dashboard - Complete site overview
    - sites://all/status - Status of all sites

    All operations require proper authentication via environment variables:
    ROCKETNET_EMAIL and ROCKETNET_PASSWORD
    """
)

# Register tools
mcp.tool(list_sites)
mcp.tool(get_site)
mcp.tool(create_site)
mcp.tool(update_site)
mcp.tool(delete_site)
mcp.tool(get_site_status)
mcp.tool(clone_site)
mcp.tool(get_site_settings)
mcp.tool(update_site_settings)
mcp.tool(list_locations)
mcp.tool(get_location_info)
mcp.tool(list_plans)
mcp.tool(get_plan_details)
mcp.tool(change_site_plan)

# Register resources
@mcp.resource("site://{site_id}/dashboard")
async def site_dashboard_resource(site_id: str) -> str:
    """Get complete dashboard for a specific site."""
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            return await get_site_dashboard(client, site_id)
    except Exception as e:
        return format_error(f"Failed to get site dashboard: {str(e)}")

@mcp.resource("sites://all/status")
async def all_sites_status_resource() -> str:
    """Get status overview of all sites."""
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            return await get_all_sites_status(client)
    except Exception as e:
        return format_error(f"Failed to get sites status: {str(e)}")

# Optional: Local testing
if __name__ == "__main__":
    import asyncio
    import logging

    logging.basicConfig(level=logging.INFO)

    # For local testing only
    from dotenv import load_dotenv
    load_dotenv()

    asyncio.run(mcp.run())