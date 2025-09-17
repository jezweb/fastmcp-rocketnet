"""
WordPress Management Tools for Rocket.net
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add parent directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import make_api_request
from utils import format_success, format_error, format_warning


async def list_plugins(
    site_id: str,
    status: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all installed plugins for a WordPress site.

    Args:
        site_id: The ID of the site
        status: Filter by status (active, inactive, all)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of installed plugins with their details
    """
    try:
        params = {}
        if status:
            params["status"] = status

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/plugins",
            params=params,
            username=username,
            password=password
        )
        plugins = response.get("plugins", response.get("data", []))

        formatted_plugins = []
        for plugin in plugins:
            formatted_plugins.append({
                "name": plugin.get("name"),
                "slug": plugin.get("slug"),
                "version": plugin.get("version"),
                "status": plugin.get("status", "inactive"),
                "update_available": plugin.get("update_available", False),
                "latest_version": plugin.get("latest_version"),
                "author": plugin.get("author"),
                "description": plugin.get("description")
            })

        return format_success(
            f"Found {len(formatted_plugins)} plugins for site {site_id}",
            {
                "plugins": formatted_plugins,
                "count": len(formatted_plugins),
                "active_count": sum(1 for p in formatted_plugins if p["status"] == "active"),
                "updates_available": sum(1 for p in formatted_plugins if p["update_available"])
            }
        )

    except Exception as e:
        return format_error(f"Failed to list plugins: {str(e)}")


async def install_plugin(
    site_id: str,
    plugin_slug: str,
    activate: bool = True,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Install a WordPress plugin from the repository.

    Args:
        site_id: The ID of the site
        plugin_slug: The plugin slug from WordPress.org repository
        activate: Whether to activate the plugin after installation
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the installed plugin
    """
    try:
        payload = {
            "slug": plugin_slug,
            "activate": activate
        }

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/plugins",
            json_data=payload,
            username=username,
            password=password
        )
        plugin = response.get("plugin", response.get("data", response))

        return format_success(
            f"Plugin {plugin_slug} installed successfully",
            {
                "plugin_name": plugin.get("name", plugin_slug),
                "version": plugin.get("version"),
                "activated": activate,
                "status": plugin.get("status"),
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to install plugin {plugin_slug}: {str(e)}")


async def update_plugins(
    site_id: str,
    plugin_slugs: Optional[List[str]] = None,
    update_all: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update WordPress plugins to their latest versions.

    Args:
        site_id: The ID of the site
        plugin_slugs: List of plugin slugs to update (optional)
        update_all: Update all plugins with available updates
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about updated plugins
    """
    try:
        payload = {}

        if update_all:
            payload["update_all"] = True
        elif plugin_slugs:
            payload["plugins"] = plugin_slugs
        else:
            return format_warning("Specify plugin_slugs or set update_all=True")

        response = await make_api_request(
            method="PUT",
            endpoint=f"/sites/{site_id}/plugins",
            json_data=payload,
            username=username,
            password=password
        )
        result = response.get("result", response.get("data", response))

        return format_success(
            "Plugins updated successfully",
            {
                "site_id": site_id,
                "updated_plugins": result.get("updated", []),
                "updated_count": result.get("updated_count", 0),
                "failed_updates": result.get("failed", []),
                "message": "Plugin updates completed"
            }
        )

    except Exception as e:
        return format_error(f"Failed to update plugins: {str(e)}")


async def activate_plugin(
    site_id: str,
    plugin_slug: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Activate an installed WordPress plugin.

    Args:
        site_id: The ID of the site
        plugin_slug: The plugin slug to activate
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of plugin activation
    """
    try:
        payload = {
            "slug": plugin_slug,
            "action": "activate"
        }

        response = await make_api_request(
            method="PATCH",
            endpoint=f"/sites/{site_id}/plugins",
            json_data=payload,
            username=username,
            password=password
        )

        return format_success(
            f"Plugin {plugin_slug} activated",
            {
                "plugin_slug": plugin_slug,
                "status": "active",
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to activate plugin {plugin_slug}: {str(e)}")


async def deactivate_plugin(
    site_id: str,
    plugin_slug: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Deactivate an installed WordPress plugin.

    Args:
        site_id: The ID of the site
        plugin_slug: The plugin slug to deactivate
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of plugin deactivation
    """
    try:
        payload = {
            "slug": plugin_slug,
            "action": "deactivate"
        }

        response = await make_api_request(
            method="PATCH",
            endpoint=f"/sites/{site_id}/plugins",
            json_data=payload,
            username=username,
            password=password
        )

        return format_success(
            f"Plugin {plugin_slug} deactivated",
            {
                "plugin_slug": plugin_slug,
                "status": "inactive",
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to deactivate plugin {plugin_slug}: {str(e)}")


async def delete_plugin(
    site_id: str,
    plugin_slug: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a WordPress plugin from the site.

    Args:
        site_id: The ID of the site
        plugin_slug: The plugin slug to delete
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of plugin deletion
    """
    try:
        params = {"slug": plugin_slug}

        await make_api_request(
            method="DELETE",
            endpoint=f"/sites/{site_id}/plugins",
            params=params,
            username=username,
            password=password
        )

        return format_success(
            f"Plugin {plugin_slug} deleted",
            {
                "deleted_plugin": plugin_slug,
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to delete plugin {plugin_slug}: {str(e)}")


async def search_plugins(
    site_id: str,
    search_term: str,
    limit: int = 10,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for WordPress plugins in the repository.

    Args:
        site_id: The ID of the site
        search_term: Search query for plugins
        limit: Maximum number of results
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of plugins matching the search
    """
    try:
        params = {
            "search": search_term,
            "limit": limit
        }

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/plugins/search",
            params=params,
            username=username,
            password=password
        )
        plugins = response.get("plugins", response.get("data", []))

        formatted_results = []
        for plugin in plugins[:limit]:
            formatted_results.append({
                "name": plugin.get("name"),
                "slug": plugin.get("slug"),
                "rating": plugin.get("rating"),
                "num_ratings": plugin.get("num_ratings"),
                "active_installs": plugin.get("active_installs"),
                "last_updated": plugin.get("last_updated"),
                "tested_up_to": plugin.get("tested_up_to"),
                "short_description": plugin.get("short_description")
            })

        return format_success(
            f"Found {len(formatted_results)} plugins matching '{search_term}'",
            {
                "search_term": search_term,
                "results": formatted_results,
                "count": len(formatted_results)
            }
        )

    except Exception as e:
        return format_error(f"Failed to search plugins: {str(e)}")


async def list_themes(
    site_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all installed themes for a WordPress site.

    Args:
        site_id: The ID of the site
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of installed themes
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/themes",
            username=username,
            password=password
        )
        themes = response.get("themes", response.get("data", []))

        formatted_themes = []
        for theme in themes:
            formatted_themes.append({
                "name": theme.get("name"),
                "slug": theme.get("slug"),
                "version": theme.get("version"),
                "status": theme.get("status", "inactive"),
                "active": theme.get("active", False),
                "update_available": theme.get("update_available", False),
                "author": theme.get("author"),
                "screenshot": theme.get("screenshot")
            })

        active_theme = next((t for t in formatted_themes if t["active"]), None)

        return format_success(
            f"Found {len(formatted_themes)} themes for site {site_id}",
            {
                "themes": formatted_themes,
                "count": len(formatted_themes),
                "active_theme": active_theme.get("name") if active_theme else None,
                "updates_available": sum(1 for t in formatted_themes if t["update_available"])
            }
        )

    except Exception as e:
        return format_error(f"Failed to list themes: {str(e)}")


async def install_theme(
    site_id: str,
    theme_slug: str,
    activate: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Install a WordPress theme from the repository.

    Args:
        site_id: The ID of the site
        theme_slug: The theme slug from WordPress.org repository
        activate: Whether to activate the theme after installation
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the installed theme
    """
    try:
        payload = {
            "slug": theme_slug,
            "activate": activate
        }

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/themes",
            json_data=payload,
            username=username,
            password=password
        )
        theme = response.get("theme", response.get("data", response))

        return format_success(
            f"Theme {theme_slug} installed successfully",
            {
                "theme_name": theme.get("name", theme_slug),
                "version": theme.get("version"),
                "activated": activate,
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to install theme {theme_slug}: {str(e)}")


async def activate_theme(
    site_id: str,
    theme_slug: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Activate an installed WordPress theme.

    Args:
        site_id: The ID of the site
        theme_slug: The theme slug to activate
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of theme activation
    """
    try:
        payload = {
            "slug": theme_slug,
            "action": "activate"
        }

        response = await make_api_request(
            method="PATCH",
            endpoint=f"/sites/{site_id}/themes",
            json_data=payload,
            username=username,
            password=password
        )

        return format_success(
            f"Theme {theme_slug} activated",
            {
                "theme_slug": theme_slug,
                "status": "active",
                "site_id": site_id,
                "message": "Theme is now the active theme for the site"
            }
        )

    except Exception as e:
        return format_error(f"Failed to activate theme {theme_slug}: {str(e)}")


async def delete_theme(
    site_id: str,
    theme_slug: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a WordPress theme from the site.

    Args:
        site_id: The ID of the site
        theme_slug: The theme slug to delete
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of theme deletion
    """
    try:
        params = {"slug": theme_slug}

        await make_api_request(
            method="DELETE",
            endpoint=f"/sites/{site_id}/themes",
            params=params,
            username=username,
            password=password
        )

        return format_success(
            f"Theme {theme_slug} deleted",
            {
                "deleted_theme": theme_slug,
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to delete theme {theme_slug}: {str(e)}")


async def search_themes(
    site_id: str,
    search_term: str,
    limit: int = 10,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for WordPress themes in the repository.

    Args:
        site_id: The ID of the site
        search_term: Search query for themes
        limit: Maximum number of results
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of themes matching the search
    """
    try:
        params = {
            "search": search_term,
            "limit": limit
        }

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/themes/search",
            params=params,
            username=username,
            password=password
        )
        themes = response.get("themes", response.get("data", []))

        formatted_results = []
        for theme in themes[:limit]:
            formatted_results.append({
                "name": theme.get("name"),
                "slug": theme.get("slug"),
                "rating": theme.get("rating"),
                "num_ratings": theme.get("num_ratings"),
                "active_installs": theme.get("active_installs"),
                "last_updated": theme.get("last_updated"),
                "tested_up_to": theme.get("tested_up_to"),
                "short_description": theme.get("description", theme.get("short_description")),
                "author": theme.get("author"),
                "screenshot": theme.get("screenshot")
            })

        return format_success(
            f"Found {len(formatted_results)} themes matching '{search_term}'",
            {
                "search_term": search_term,
                "results": formatted_results,
                "count": len(formatted_results)
            }
        )

    except Exception as e:
        return format_error(f"Failed to search themes: {str(e)}")


async def update_themes(
    site_id: str,
    theme_slugs: Optional[List[str]] = None,
    update_all: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update WordPress themes to their latest versions.

    Args:
        site_id: The ID of the site
        theme_slugs: List of theme slugs to update (optional)
        update_all: Update all themes with available updates
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about updated themes
    """
    try:
        payload = {}

        if update_all:
            payload["update_all"] = True
        elif theme_slugs:
            payload["themes"] = theme_slugs
        else:
            return format_warning("Specify theme_slugs or set update_all=True")

        response = await make_api_request(
            method="PUT",
            endpoint=f"/sites/{site_id}/themes",
            json_data=payload,
            username=username,
            password=password
        )
        result = response.get("result", response.get("data", response))

        return format_success(
            "Themes updated successfully",
            {
                "site_id": site_id,
                "updated_themes": result.get("updated", []),
                "updated_count": result.get("updated_count", 0),
                "failed_updates": result.get("failed", []),
                "message": "Theme updates completed"
            }
        )

    except Exception as e:
        return format_error(f"Failed to update themes: {str(e)}")


async def get_wordpress_status(
    site_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get WordPress installation status and health.

    Args:
        site_id: The ID of the site
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        WordPress status information
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/wp/status",
            username=username,
            password=password
        )
        status = response.get("status", response.get("data", response))

        return format_success(
            "WordPress status retrieved",
            {
                "site_id": site_id,
                "wordpress_version": status.get("wordpress_version"),
                "php_version": status.get("php_version"),
                "mysql_version": status.get("mysql_version"),
                "is_multisite": status.get("is_multisite", False),
                "debug_mode": status.get("debug_mode", False),
                "database_size": status.get("database_size"),
                "total_posts": status.get("total_posts"),
                "total_pages": status.get("total_pages"),
                "total_users": status.get("total_users"),
                "plugin_count": status.get("plugin_count"),
                "theme_count": status.get("theme_count"),
                "last_update_check": status.get("last_update_check"),
                "auto_updates": status.get("auto_updates", {})
            }
        )

    except Exception as e:
        return format_error(f"Failed to get WordPress status: {str(e)}")


async def get_wordpress_login_url(
    site_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a one-time SSO login URL for WordPress admin.

    Args:
        site_id: The ID of the site
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        SSO login URL for WordPress admin
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/wp_login",
            username=username,
            password=password
        )
        login_info = response.get("login", response.get("data", response))

        return format_success(
            "WordPress SSO login URL generated",
            {
                "site_id": site_id,
                "login_url": login_info.get("url"),
                "expires_at": login_info.get("expires_at"),
                "message": "This is a one-time login URL that expires after use or timeout"
            }
        )

    except Exception as e:
        return format_error(f"Failed to get WordPress login URL: {str(e)}")


async def run_wpcli_command(
    site_id: str,
    command: str,
    args: Optional[List[str]] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a WP-CLI command on the WordPress site.

    Args:
        site_id: The ID of the site
        command: The WP-CLI command to run (e.g., "cache flush", "user list")
        args: Additional arguments for the command
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Command output and execution result
    """
    try:
        payload = {
            "command": command
        }

        if args:
            payload["args"] = args

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/wpcli",
            json_data=payload,
            username=username,
            password=password
        )
        result = response.get("result", response.get("data", response))

        return format_success(
            f"WP-CLI command executed: {command}",
            {
                "site_id": site_id,
                "command": command,
                "args": args,
                "output": result.get("output"),
                "exit_code": result.get("exit_code", 0),
                "execution_time": result.get("execution_time")
            }
        )

    except Exception as e:
        return format_error(f"Failed to execute WP-CLI command: {str(e)}")