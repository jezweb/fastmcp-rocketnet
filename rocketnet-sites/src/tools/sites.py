"""
Site Management Tools for Rocket.net
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add parent directory to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from rocketnet_shared import (
    make_api_request,
    format_success,
    format_error,
    format_warning,
    format_site_info,
)


async def list_sites(
    status: Optional[str] = None,
    plan: Optional[str] = None,
    location: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all sites in your Rocket.net account.

    Args:
        status: Filter by site status (active, suspended, pending)
        plan: Filter by hosting plan
        location: Filter by data center location
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of sites with their basic information
    """
    try:
        params = {}
        if status:
            params["status"] = status
        if plan:
            params["plan"] = plan
        if location:
            params["location"] = location

        response = await make_api_request(
            method="GET",
            endpoint="/sites",
            username=username,
            password=password,
            params=params
        )

        # Format site information
        sites = response.get("sites", response.get("data", []))
        formatted_sites = [format_site_info(site) for site in sites]

        return format_success(
            f"Found {len(formatted_sites)} sites",
            {"sites": formatted_sites, "count": len(formatted_sites)}
        )

    except Exception as e:
        return format_error(f"Failed to list sites: {str(e)}")


async def get_site(
    site_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific site.

    Args:
        site_id: The ID of the site to retrieve
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Detailed site information including configuration and status
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}",
            username=username,
            password=password
        )
        site = response.get("site", response.get("data", response))

        return format_success(
            f"Retrieved site: {site.get('name', site_id)}",
            format_site_info(site)
        )

    except Exception as e:
        return format_error(f"Failed to get site {site_id}: {str(e)}")


async def create_site(
    name: str,
    domain: str,
    plan: str = "starter",
    location: str = "us-east-1",
    wordpress_version: Optional[str] = None,
    php_version: Optional[str] = "8.2",
    admin_email: Optional[str] = None,
    admin_username: Optional[str] = "admin",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new WordPress site on Rocket.net.

    Args:
        name: Site name/title
        domain: Primary domain for the site
        plan: Hosting plan (starter, pro, business, agency)
        location: Data center location
        wordpress_version: WordPress version to install (latest if not specified)
        php_version: PHP version (7.4, 8.0, 8.1, 8.2)
        admin_email: WordPress admin email
        admin_username: WordPress admin username
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the created site
    """
    try:
        payload = {
            "name": name,
            "domain": domain,
            "plan": plan,
            "location": location,
            "php_version": php_version,
            "admin_username": admin_username
        }

        if wordpress_version:
            payload["wordpress_version"] = wordpress_version
        if admin_email:
            payload["admin_email"] = admin_email

        response = await make_api_request(
            method="POST",
            endpoint="/sites",
            username=username,
            password=password,
            json_data=payload
        )

        site = response.get("site", response.get("data", response))

        return format_success(
            f"Site '{name}' created successfully",
            {
                "site": format_site_info(site),
                "login_url": f"https://{domain}/wp-admin",
                "temporary_url": site.get("temporary_url"),
                "setup_status": "Site is being provisioned. This may take a few minutes."
            }
        )

    except Exception as e:
        return format_error(f"Failed to create site: {str(e)}")


async def update_site(
    site_id: str,
    name: Optional[str] = None,
    php_version: Optional[str] = None,
    wordpress_autoupdate: Optional[bool] = None,
    plugin_autoupdate: Optional[bool] = None,
    theme_autoupdate: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Update site configuration.

    Args:
        site_id: The ID of the site to update
        name: New site name
        php_version: PHP version to switch to
        wordpress_autoupdate: Enable/disable WordPress auto-updates
        plugin_autoupdate: Enable/disable plugin auto-updates
        theme_autoupdate: Enable/disable theme auto-updates

    Returns:
        Updated site information
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            payload = {}

            if name:
                payload["name"] = name
            if php_version:
                payload["php_version"] = php_version
            if wordpress_autoupdate is not None:
                payload["wordpress_autoupdate"] = wordpress_autoupdate
            if plugin_autoupdate is not None:
                payload["plugin_autoupdate"] = plugin_autoupdate
            if theme_autoupdate is not None:
                payload["theme_autoupdate"] = theme_autoupdate

            if not payload:
                return format_warning("No updates provided")

            response = await client.patch(f"/sites/{site_id}", payload)
            site = response.get("site", response.get("data", response))

            return format_success(
                f"Site {site_id} updated successfully",
                format_site_info(site)
            )

    except Exception as e:
        return format_error(f"Failed to update site {site_id}: {str(e)}")


async def delete_site(
    site_id: str,
    confirm: bool = False
) -> Dict[str, Any]:
    """
    Delete a site from Rocket.net. This action is irreversible!

    Args:
        site_id: The ID of the site to delete
        confirm: Must be True to confirm deletion

    Returns:
        Confirmation of deletion
    """
    try:
        if not confirm:
            return format_warning(
                "Site deletion requires confirmation",
                {"message": "Set confirm=True to delete the site. This action cannot be undone!"}
            )

        config = Config.from_env()
        async with RocketnetClient(config) as client:
            # Get site info first for confirmation message
            site_response = await client.get(f"/sites/{site_id}")
            site = site_response.get("site", site_response.get("data", {}))
            site_name = site.get("name", site_id)

            # Delete the site
            await client.delete(f"/sites/{site_id}")

            return format_success(
                f"Site '{site_name}' (ID: {site_id}) has been deleted",
                {"deleted_site_id": site_id, "deleted_site_name": site_name}
            )

    except Exception as e:
        return format_error(f"Failed to delete site {site_id}: {str(e)}")


async def get_site_status(site_id: str) -> Dict[str, Any]:
    """
    Get the current status and health of a site.

    Args:
        site_id: The ID of the site to check

    Returns:
        Site status including health checks and metrics
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            response = await client.get(f"/sites/{site_id}/status")

            status_data = response.get("status", response.get("data", response))

            return format_success(
                f"Site status retrieved",
                {
                    "site_id": site_id,
                    "status": status_data.get("status", "unknown"),
                    "health": status_data.get("health", "unknown"),
                    "uptime": status_data.get("uptime"),
                    "response_time": status_data.get("response_time"),
                    "ssl_status": status_data.get("ssl_status"),
                    "last_backup": status_data.get("last_backup"),
                    "disk_usage": status_data.get("disk_usage"),
                    "bandwidth_usage": status_data.get("bandwidth_usage"),
                    "php_version": status_data.get("php_version"),
                    "wordpress_version": status_data.get("wordpress_version"),
                    "issues": status_data.get("issues", [])
                }
            )

    except Exception as e:
        return format_error(f"Failed to get site status for {site_id}: {str(e)}")


async def clone_site(
    source_site_id: str,
    new_name: str,
    new_domain: str,
    location: Optional[str] = None,
    plan: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a copy of an existing site.

    Args:
        source_site_id: The ID of the site to clone
        new_name: Name for the new site
        new_domain: Domain for the new site
        location: Data center location for the new site (uses source site location if not specified)
        plan: Hosting plan for the new site (uses source site plan if not specified)

    Returns:
        Information about the cloned site
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            payload = {
                "source_site_id": source_site_id,
                "name": new_name,
                "domain": new_domain
            }

            if location:
                payload["location"] = location
            if plan:
                payload["plan"] = plan

            response = await client.post("/sites/clone", payload)
            site = response.get("site", response.get("data", response))

            return format_success(
                f"Site cloned successfully as '{new_name}'",
                {
                    "site": format_site_info(site),
                    "source_site_id": source_site_id,
                    "clone_status": "Cloning in progress. This may take several minutes.",
                    "temporary_url": site.get("temporary_url")
                }
            )

    except Exception as e:
        return format_error(f"Failed to clone site {source_site_id}: {str(e)}")


async def get_site_settings(site_id: str) -> Dict[str, Any]:
    """
    Get all settings for a site.

    Args:
        site_id: The ID of the site

    Returns:
        Complete site settings
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            response = await client.get(f"/sites/{site_id}/settings")
            settings = response.get("settings", response.get("data", response))

            return format_success(
                f"Site settings retrieved",
                settings
            )

    except Exception as e:
        return format_error(f"Failed to get site settings for {site_id}: {str(e)}")


async def update_site_settings(
    site_id: str,
    settings: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update site settings.

    Args:
        site_id: The ID of the site
        settings: Dictionary of settings to update

    Returns:
        Updated settings
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            response = await client.patch(f"/sites/{site_id}/settings", settings)
            updated_settings = response.get("settings", response.get("data", response))

            return format_success(
                f"Site settings updated",
                updated_settings
            )

    except Exception as e:
        return format_error(f"Failed to update site settings for {site_id}: {str(e)}")