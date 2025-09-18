"""
Rocket.net Backup Management MCP Server
========================================
Comprehensive backup and disaster recovery operations.
"""

import os
import sys
from pathlib import Path

from fastmcp import FastMCP
from utils import format_success, format_error

# Import tools
from tools.backups import (
    create_backup,
    list_backups,
    get_backup,
    restore_backup,
    download_backup,
    delete_backup,
    test_restore,
    schedule_backup,
    get_backup_schedule,
    update_backup_schedule,
    delete_backup_schedule,
    # Cloud backups
    list_cloud_backups,
    create_cloud_backup,
    get_cloud_backup,
    delete_cloud_backup,
    download_cloud_backup,
    restore_cloud_backup,
)

# Initialize FastMCP server - MUST be at module level for FastMCP Cloud
mcp = FastMCP(
    name="rocketnet-backups",
    instructions="""
    This server provides comprehensive backup and recovery tools for Rocket.net sites.

    Available tools:
    - create_backup: Create a manual backup of a site
    - list_backups: List all backups for a site
    - get_backup: Get details of a specific backup
    - restore_backup: Restore a site from a backup
    - download_backup: Get a download link for a backup
    - delete_backup: Delete a specific backup
    - test_restore: Test restoration process without affecting live site
    - schedule_backup: Set up automatic backup schedule
    - get_backup_schedule: Get current backup schedule
    - update_backup_schedule: Modify backup schedule
    - delete_backup_schedule: Remove automatic backups

    Cloud Backup Tools:
    - list_cloud_backups: List cloud backups
    - create_cloud_backup: Create encrypted cloud backup
    - get_cloud_backup: Get cloud backup details
    - delete_cloud_backup: Delete cloud backup
    - download_cloud_backup: Get download link
    - restore_cloud_backup: Restore from cloud

    Backup Types:
    - full: Complete site backup including files and database
    - database: Database only backup
    - files: Files only backup
    - incremental: Incremental backup since last full backup

    All operations require proper authentication via environment variables:
    ROCKETNET_USERNAME and ROCKETNET_PASSWORD
    """
)

# Register tools
mcp.tool(create_backup)
mcp.tool(list_backups)
mcp.tool(get_backup)
mcp.tool(restore_backup)
mcp.tool(download_backup)
mcp.tool(delete_backup)
mcp.tool(test_restore)
mcp.tool(schedule_backup)
mcp.tool(get_backup_schedule)
mcp.tool(update_backup_schedule)
mcp.tool(delete_backup_schedule)

# Cloud backup tools
mcp.tool(list_cloud_backups)
mcp.tool(create_cloud_backup)
mcp.tool(get_cloud_backup)
mcp.tool(delete_cloud_backup)
mcp.tool(download_cloud_backup)
mcp.tool(restore_cloud_backup)

# Register resource for backup status
@mcp.resource("backups://{site_id}/recent")
async def recent_backups_resource(site_id: str) -> str:
    """Get recent backups for a site."""
    try:
        from auth import make_api_request
        import json

        response = await make_api_request(
            "GET",
            f"/sites/{site_id}/backups",
            params={"limit": 10}
        )
        backups = response.get("backups", response.get("data", []))

        return json.dumps({
            "site_id": site_id,
            "recent_backups": backups,
            "count": len(backups)
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