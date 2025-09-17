"""
Rocket.net Domain Management MCP Server
========================================
Domain configuration, DNS, and SSL certificate management.
"""

import os
import sys
from pathlib import Path

from fastmcp import FastMCP
from utils import format_success, format_error

# Import tools
from tools.domains import (
    list_domains,
    add_domain,
    remove_domain,
    get_main_domain,
    set_main_domain,
    replace_main_domain,
    update_main_domain_ssl,
    get_domain_edge_settings,
    update_domain_edge_settings,
)

# Initialize FastMCP server - MUST be at module level for FastMCP Cloud
mcp = FastMCP(
    name="rocketnet-domains",
    instructions="""
    This server provides domain management tools for Rocket.net sites.

    Available tools:
    - list_domains: List all additional domains (aliases) for a site
    - add_domain: Add a new domain alias to a site
    - remove_domain: Remove a domain alias from a site
    - get_main_domain: Get main domain information and SSL status
    - set_main_domain: Set the main domain for a site
    - replace_main_domain: Replace the current main domain
    - update_main_domain_ssl: Update SSL settings for main domain
    - get_domain_edge_settings: Get CDN/edge settings for a domain
    - update_domain_edge_settings: Update CDN/edge settings

    Domain Features:
    - SSL certificate management (Let's Encrypt, ZeroSSL)
    - HTTP or DNS validation methods
    - Edge/CDN configuration
    - Domain aliases and redirects

    Resources:
    - domains://{site_id}/all - List all domains for a site
    - domain://{site_id}/main - Main domain information

    All operations require proper authentication via environment variables:
    ROCKETNET_EMAIL and ROCKETNET_PASSWORD
    """
)

# Register tools
mcp.tool(list_domains)
mcp.tool(add_domain)
mcp.tool(remove_domain)
mcp.tool(get_main_domain)
mcp.tool(set_main_domain)
mcp.tool(replace_main_domain)
mcp.tool(update_main_domain_ssl)
mcp.tool(get_domain_edge_settings)
mcp.tool(update_domain_edge_settings)

# Register resources
@mcp.resource("domains://{site_id}/all")
async def all_domains_resource(site_id: str) -> str:
    """Get all domains (main and additional) for a site."""
    try:
        from auth import make_api_request
        import json

        # Get main domain
        main_response = await make_api_request("GET", f"/sites/{site_id}/maindomain")
        main_domain = main_response.get("domain", main_response.get("data", {}))

        # Get additional domains
        additional_response = await make_api_request("GET", f"/sites/{site_id}/domains")
        additional_domains = additional_response.get("domains", additional_response.get("data", []))

        # Combine results
        all_domains = {
            "site_id": site_id,
            "main_domain": main_domain,
            "additional_domains": additional_domains,
            "total_domains": 1 + len(additional_domains)
        }

        return json.dumps(all_domains, indent=2)
    except Exception as e:
        import json
        return json.dumps({"error": str(e)}, indent=2)

@mcp.resource("domain://{site_id}/main")
async def main_domain_resource(site_id: str) -> str:
    """Get main domain details including SSL status."""
    try:
        from auth import make_api_request
        import json

        response = await make_api_request("GET", f"/sites/{site_id}/maindomain")
        domain = response.get("domain", response.get("data", response))

        return json.dumps({
            "site_id": site_id,
            "main_domain": domain
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