"""
Rocket.net WordPress Management MCP Server
===========================================
WordPress-specific operations for plugins, themes, and WP-CLI.
"""

import os
import sys
from pathlib import Path

from fastmcp import FastMCP
from utils import format_success, format_error

# Import tools
from tools.wordpress import (
    list_plugins,
    install_plugin,
    update_plugins,
    activate_plugin,
    deactivate_plugin,
    delete_plugin,
    search_plugins,
    list_themes,
    install_theme,
    activate_theme,
    delete_theme,
    get_wordpress_status,
    get_wordpress_login_url,
    run_wpcli_command,
)

# Initialize FastMCP server - MUST be at module level for FastMCP Cloud
mcp = FastMCP(
    name="rocketnet-wordpress",
    instructions="""
    This server provides WordPress-specific management tools for Rocket.net sites.

    Available tools:
    - list_plugins: List all installed plugins
    - install_plugin: Install a plugin from WordPress.org
    - update_plugins: Update plugins to latest versions
    - activate_plugin: Activate an installed plugin
    - deactivate_plugin: Deactivate a plugin
    - delete_plugin: Remove a plugin
    - search_plugins: Search WordPress.org for plugins
    - list_themes: List all installed themes
    - install_theme: Install a theme from WordPress.org
    - activate_theme: Activate an installed theme
    - delete_theme: Remove a theme
    - get_wordpress_status: Get WordPress installation health
    - get_wordpress_login_url: Generate SSO login URL
    - run_wpcli_command: Execute WP-CLI commands

    WordPress Features:
    - Plugin management (install, update, activate, delete)
    - Theme management
    - WP-CLI command execution
    - WordPress health monitoring
    - One-click SSO login

    Resources:
    - wordpress://{site_id}/status - Complete WordPress status
    - plugins://{site_id}/updates - Plugins needing updates

    All operations require proper authentication via environment variables:
    ROCKETNET_EMAIL and ROCKETNET_PASSWORD
    """
)

# Register tools
mcp.tool(list_plugins)
mcp.tool(install_plugin)
mcp.tool(update_plugins)
mcp.tool(activate_plugin)
mcp.tool(deactivate_plugin)
mcp.tool(delete_plugin)
mcp.tool(search_plugins)
mcp.tool(list_themes)
mcp.tool(install_theme)
mcp.tool(activate_theme)
mcp.tool(delete_theme)
mcp.tool(get_wordpress_status)
mcp.tool(get_wordpress_login_url)
mcp.tool(run_wpcli_command)

# Register resources
@mcp.resource("wordpress://{site_id}/status")
async def wordpress_status_resource(site_id: str) -> str:
    """Get complete WordPress status for a site."""
    try:
        from auth import make_api_request
        import json

        # Get WordPress status
        status_response = await make_api_request("GET", f"/sites/{site_id}/wp-status")

        # Get plugin info
        plugins_response = await make_api_request("GET", f"/sites/{site_id}/plugins")

        # Get theme info
        themes_response = await make_api_request("GET", f"/sites/{site_id}/themes")

        status = {
            "site_id": site_id,
            "wordpress": status_response.get("status", status_response.get("data", {})),
            "plugins_summary": {
                "total": len(plugins_response.get("plugins", [])),
                "active": sum(1 for p in plugins_response.get("plugins", []) if p.get("status") == "active"),
                "updates_available": sum(1 for p in plugins_response.get("plugins", []) if p.get("update_available"))
            },
            "themes_summary": {
                "total": len(themes_response.get("themes", [])),
                "active": next((t.get("name") for t in themes_response.get("themes", []) if t.get("active")), None)
            }
        }

        return json.dumps(status, indent=2)
    except Exception as e:
        import json
        return json.dumps({"error": str(e)}, indent=2)

@mcp.resource("plugins://{site_id}/updates")
async def plugin_updates_resource(site_id: str) -> str:
    """Get plugins needing updates for a site."""
    try:
        from auth import make_api_request
        import json

        response = await make_api_request("GET", f"/sites/{site_id}/plugins")
        plugins = response.get("plugins", response.get("data", []))

        updates_needed = [
            {
                "name": p.get("name"),
                "slug": p.get("slug"),
                "current_version": p.get("version"),
                "latest_version": p.get("latest_version")
            }
            for p in plugins if p.get("update_available")
        ]

        return json.dumps({
            "site_id": site_id,
            "updates_needed": updates_needed,
            "count": len(updates_needed)
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