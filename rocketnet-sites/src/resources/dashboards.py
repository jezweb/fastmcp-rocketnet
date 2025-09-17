"""
Dashboard Resources for Rocket.net Sites
"""

import json
from typing import Dict, Any
from datetime import datetime

from rocketnet_shared import RocketnetClient, format_datetime


async def get_site_dashboard(client: RocketnetClient, site_id: str) -> str:
    """
    Get a complete dashboard overview for a specific site.

    Args:
        client: RocketnetClient instance
        site_id: The ID of the site

    Returns:
        JSON string with complete site dashboard
    """
    try:
        # Fetch multiple data points in parallel
        site_data = await client.get(f"/sites/{site_id}")
        status_data = await client.get(f"/sites/{site_id}/status")

        site = site_data.get("site", site_data.get("data", {}))
        status = status_data.get("status", status_data.get("data", {}))

        dashboard = {
            "site_info": {
                "id": site.get("id"),
                "name": site.get("name"),
                "domain": site.get("domain"),
                "created_at": format_datetime(site.get("created_at")),
                "plan": site.get("plan"),
                "location": site.get("location")
            },
            "status": {
                "overall": status.get("status", "unknown"),
                "health": status.get("health", "unknown"),
                "uptime": status.get("uptime"),
                "last_check": format_datetime(status.get("last_check"))
            },
            "performance": {
                "response_time": status.get("response_time"),
                "cdn_hit_rate": status.get("cdn_hit_rate"),
                "page_speed_score": status.get("page_speed_score")
            },
            "resources": {
                "disk_usage": {
                    "used": status.get("disk_usage", {}).get("used"),
                    "total": status.get("disk_usage", {}).get("total"),
                    "percentage": status.get("disk_usage", {}).get("percentage")
                },
                "bandwidth": {
                    "used": status.get("bandwidth_usage", {}).get("used"),
                    "limit": status.get("bandwidth_usage", {}).get("limit"),
                    "percentage": status.get("bandwidth_usage", {}).get("percentage")
                }
            },
            "wordpress": {
                "version": site.get("wordpress_version"),
                "php_version": site.get("php_version"),
                "plugins_count": site.get("plugins_count"),
                "themes_count": site.get("themes_count"),
                "auto_updates": {
                    "core": site.get("wordpress_autoupdate"),
                    "plugins": site.get("plugin_autoupdate"),
                    "themes": site.get("theme_autoupdate")
                }
            },
            "security": {
                "ssl_enabled": site.get("ssl_enabled", True),
                "ssl_expiry": format_datetime(site.get("ssl_expiry")),
                "firewall_enabled": site.get("firewall_enabled", True),
                "last_backup": format_datetime(status.get("last_backup"))
            },
            "recent_activity": status.get("recent_activity", []),
            "issues": status.get("issues", []),
            "recommendations": status.get("recommendations", [])
        }

        return json.dumps(dashboard, indent=2)

    except Exception as e:
        return json.dumps({
            "error": f"Failed to generate dashboard: {str(e)}",
            "site_id": site_id
        }, indent=2)


async def get_all_sites_status(client: RocketnetClient) -> str:
    """
    Get status overview of all sites.

    Returns:
        JSON string with status of all sites
    """
    try:
        # Get all sites
        sites_response = await client.get("/sites")
        sites = sites_response.get("sites", sites_response.get("data", []))

        sites_status = {
            "summary": {
                "total_sites": len(sites),
                "active": 0,
                "issues": 0,
                "maintenance": 0
            },
            "sites": []
        }

        # Get status for each site
        for site in sites:
            site_id = site.get("id")
            try:
                status_response = await client.get(f"/sites/{site_id}/status")
                status = status_response.get("status", status_response.get("data", {}))

                site_status = {
                    "id": site_id,
                    "name": site.get("name"),
                    "domain": site.get("domain"),
                    "status": status.get("status", "unknown"),
                    "health": status.get("health", "unknown"),
                    "uptime": status.get("uptime"),
                    "response_time": status.get("response_time"),
                    "issues": len(status.get("issues", [])),
                    "last_check": format_datetime(status.get("last_check"))
                }

                # Update summary counters
                if site_status["status"] == "active":
                    sites_status["summary"]["active"] += 1
                if site_status["issues"] > 0:
                    sites_status["summary"]["issues"] += 1
                if site_status["status"] == "maintenance":
                    sites_status["summary"]["maintenance"] += 1

                sites_status["sites"].append(site_status)

            except Exception as e:
                # If we can't get status for a site, include basic info
                sites_status["sites"].append({
                    "id": site_id,
                    "name": site.get("name"),
                    "domain": site.get("domain"),
                    "status": "error",
                    "error": str(e)
                })

        # Sort sites by status (issues first, then by name)
        sites_status["sites"].sort(
            key=lambda x: (
                x.get("status") != "error",
                -x.get("issues", 0),
                x.get("name", "")
            )
        )

        sites_status["generated_at"] = datetime.utcnow().isoformat()

        return json.dumps(sites_status, indent=2)

    except Exception as e:
        return json.dumps({
            "error": f"Failed to get sites status: {str(e)}"
        }, indent=2)