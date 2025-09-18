"""
Rocket.net Site Access Management MCP Server
=============================================
SSH keys, FTP accounts, file management, staging, and access control.
"""

import os
import sys
from pathlib import Path

from fastmcp import FastMCP
from utils import format_success, format_error

# Import tools
from tools.access import (
    # SSH Key Management
    list_ssh_keys,
    add_ssh_key,
    authorize_ssh_key,
    delete_ssh_key,
    # FTP Account Management
    list_ftp_accounts,
    create_ftp_account,
    delete_ftp_account,
    # File Management
    list_files,
    upload_file,
    delete_file,
    compress_files,
    extract_archive,
    # Staging Sites
    create_staging_site,
    publish_staging,
    delete_staging_site,
    # phpMyAdmin
    get_phpmyadmin_login,
    # Password Protection
    get_password_protection_status,
    enable_password_protection,
    add_password_user,
)

# Initialize FastMCP server - MUST be at module level for FastMCP Cloud
mcp = FastMCP(
    name="rocketnet-access",
    instructions="""
    This server provides site access management tools for Rocket.net sites.

    Available tools:

    SSH Key Management:
    - list_ssh_keys: List SSH keys for a site
    - add_ssh_key: Add an SSH key
    - authorize_ssh_key: Authorize an SSH key
    - delete_ssh_key: Remove an SSH key

    FTP Account Management:
    - list_ftp_accounts: List FTP accounts
    - create_ftp_account: Create FTP account
    - delete_ftp_account: Remove FTP account

    File Management:
    - list_files: Browse site files
    - upload_file: Upload files to site
    - delete_file: Delete files
    - compress_files: Create archives
    - extract_archive: Extract archives

    Staging Sites:
    - create_staging_site: Create staging environment
    - publish_staging: Push staging to production
    - delete_staging_site: Remove staging

    Access Tools:
    - get_phpmyadmin_login: Get phpMyAdmin SSO URL
    - get_password_protection_status: Check protection status
    - enable_password_protection: Enable site protection
    - add_password_user: Add protected access user

    Resources:
    - access://{site_id}/overview - Site access overview
    - files://{site_id}/list - Root directory listing

    All operations require proper authentication via environment variables:
    ROCKETNET_USERNAME and ROCKETNET_PASSWORD
    """
)

# Register all tools
# SSH Keys
mcp.tool(list_ssh_keys)
mcp.tool(add_ssh_key)
mcp.tool(authorize_ssh_key)
mcp.tool(delete_ssh_key)

# FTP Accounts
mcp.tool(list_ftp_accounts)
mcp.tool(create_ftp_account)
mcp.tool(delete_ftp_account)

# File Management
mcp.tool(list_files)
mcp.tool(upload_file)
mcp.tool(delete_file)
mcp.tool(compress_files)
mcp.tool(extract_archive)

# Staging
mcp.tool(create_staging_site)
mcp.tool(publish_staging)
mcp.tool(delete_staging_site)

# Access Tools
mcp.tool(get_phpmyadmin_login)
mcp.tool(get_password_protection_status)
mcp.tool(enable_password_protection)
mcp.tool(add_password_user)

# Register resources
@mcp.resource("access://{site_id}/overview")
async def access_overview_resource(site_id: str) -> str:
    """Get complete access overview for a site."""
    try:
        from auth import make_api_request
        import json

        # Get SSH keys
        ssh_response = await make_api_request("GET", f"/sites/{site_id}/ssh-keys")

        # Get FTP accounts
        ftp_response = await make_api_request("GET", f"/sites/{site_id}/ftp-accounts")

        # Get password protection status
        protection_response = await make_api_request("GET", f"/sites/{site_id}/password-protection")

        overview = {
            "site_id": site_id,
            "ssh_keys": len(ssh_response.get("ssh_keys", [])),
            "ftp_accounts": len(ftp_response.get("ftp_accounts", [])),
            "password_protection": protection_response.get("protection", {}).get("enabled", False),
            "access_methods": {
                "ssh": len(ssh_response.get("ssh_keys", [])) > 0,
                "ftp": len(ftp_response.get("ftp_accounts", [])) > 0,
                "password_protected": protection_response.get("protection", {}).get("enabled", False)
            }
        }

        return json.dumps(overview, indent=2)
    except Exception as e:
        import json
        return json.dumps({"error": str(e)}, indent=2)

@mcp.resource("files://{site_id}/list")
async def files_list_resource(site_id: str) -> str:
    """Get root directory listing for a site."""
    try:
        from auth import make_api_request
        import json

        response = await make_api_request(
            "GET",
            f"/sites/{site_id}/file-manager/files",
            params={"path": "/", "show_hidden": False}
        )

        files = response.get("files", response.get("data", []))

        return json.dumps({
            "site_id": site_id,
            "path": "/",
            "files": files[:20],  # Limit to 20 items
            "total_items": len(files)
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