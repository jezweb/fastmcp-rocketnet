"""
Domain Management Tools for Rocket.net
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add parent directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import make_api_request
from utils import format_success, format_error, format_warning


async def list_domains(
    site_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all additional domains (aliases) for a site.

    Args:
        site_id: The ID of the site
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of additional domains for the site
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/domains",
            username=username,
            password=password
        )
        domains = response.get("domains", response.get("data", []))

        return format_success(
            f"Found {len(domains)} additional domains for site {site_id}",
            {
                "domains": domains,
                "count": len(domains),
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to list domains for site {site_id}: {str(e)}")


async def add_domain(
    site_id: str,
    domain: str,
    redirect_to_primary: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add an additional domain (alias) to a site.

    Args:
        site_id: The ID of the site
        domain: The domain to add (e.g., "www.example.com")
        redirect_to_primary: Whether to redirect this domain to the primary domain
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the added domain
    """
    try:
        payload = {
            "domain": domain,
            "redirect_to_primary": redirect_to_primary
        }

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/domains",
            json_data=payload,
            username=username,
            password=password
        )
        domain_info = response.get("domain", response.get("data", response))

        return format_success(
            f"Domain {domain} added to site {site_id}",
            {
                "domain_id": domain_info.get("id"),
                "domain": domain_info.get("domain", domain),
                "status": domain_info.get("status"),
                "redirect_to_primary": domain_info.get("redirect_to_primary", redirect_to_primary),
                "ssl_status": domain_info.get("ssl_status"),
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to add domain {domain}: {str(e)}")


async def remove_domain(
    site_id: str,
    domain_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove an additional domain from a site.

    Args:
        site_id: The ID of the site
        domain_id: The ID of the domain to remove
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of domain removal
    """
    try:
        await make_api_request(
            method="DELETE",
            endpoint=f"/sites/{site_id}/domains/{domain_id}",
            username=username,
            password=password
        )

        return format_success(
            f"Domain {domain_id} removed from site {site_id}",
            {
                "site_id": site_id,
                "removed_domain_id": domain_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to remove domain {domain_id}: {str(e)}")


async def get_main_domain(
    site_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the main domain information for a site.

    Args:
        site_id: The ID of the site
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Main domain information including SSL status
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/maindomain",
            username=username,
            password=password
        )
        domain = response.get("domain", response.get("data", response))

        return format_success(
            "Main domain information retrieved",
            {
                "domain": domain.get("domain"),
                "site_id": site_id,
                "ssl_status": domain.get("ssl_status"),
                "ssl_issuer": domain.get("ssl_issuer"),
                "ssl_expires": domain.get("ssl_expires"),
                "validation_method": domain.get("validation_method"),
                "is_staging": domain.get("is_staging", False),
                "dns_pointing_to_rocket": domain.get("dns_pointing_to_rocket"),
                "cloudflare_proxied": domain.get("cloudflare_proxied")
            }
        )

    except Exception as e:
        return format_error(f"Failed to get main domain for site {site_id}: {str(e)}")


async def set_main_domain(
    site_id: str,
    domain: str,
    validation_method: str = "http",
    ssl_ca: str = "letsencrypt",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Set the main domain for a site.

    Args:
        site_id: The ID of the site
        domain: The domain to set as main (e.g., "www.example.com")
        validation_method: SSL validation method ("http" or "dns")
        ssl_ca: SSL certificate authority ("letsencrypt" or "zerossl")
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the set main domain
    """
    try:
        payload = {
            "domain": domain,
            "validation_method": validation_method,
            "ssl_ca": ssl_ca
        }

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/maindomain",
            json_data=payload,
            username=username,
            password=password
        )
        domain_info = response.get("domain", response.get("data", response))

        return format_success(
            f"Main domain set to {domain} for site {site_id}",
            {
                "domain": domain,
                "site_id": site_id,
                "validation_method": validation_method,
                "ssl_ca": ssl_ca,
                "ssl_status": domain_info.get("ssl_status"),
                "message": "DNS propagation may take up to 48 hours"
            }
        )

    except Exception as e:
        return format_error(f"Failed to set main domain {domain}: {str(e)}")


async def replace_main_domain(
    site_id: str,
    new_domain: str,
    validation_method: Optional[str] = None,
    ssl_ca: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Replace the current main domain with a new one.

    Args:
        site_id: The ID of the site
        new_domain: The new domain to set as main
        validation_method: SSL validation method (optional)
        ssl_ca: SSL certificate authority (optional)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the domain replacement
    """
    try:
        payload = {"domain": new_domain}

        if validation_method:
            payload["validation_method"] = validation_method
        if ssl_ca:
            payload["ssl_ca"] = ssl_ca

        response = await make_api_request(
            method="PUT",
            endpoint=f"/sites/{site_id}/maindomain",
            json_data=payload,
            username=username,
            password=password
        )
        domain_info = response.get("domain", response.get("data", response))

        return format_success(
            f"Main domain replaced with {new_domain} for site {site_id}",
            {
                "new_domain": new_domain,
                "site_id": site_id,
                "previous_domain": domain_info.get("previous_domain"),
                "ssl_status": domain_info.get("ssl_status"),
                "message": "Site is now accessible at the new domain"
            }
        )

    except Exception as e:
        return format_error(f"Failed to replace main domain with {new_domain}: {str(e)}")


async def update_main_domain_ssl(
    site_id: str,
    validation_method: Optional[str] = None,
    ssl_ca: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update SSL settings for the main domain.

    Args:
        site_id: The ID of the site
        validation_method: New SSL validation method ("http" or "dns")
        ssl_ca: New SSL certificate authority ("letsencrypt" or "zerossl")
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Updated SSL configuration
    """
    try:
        payload = {}

        if validation_method:
            payload["validation_method"] = validation_method
        if ssl_ca:
            payload["ssl_ca"] = ssl_ca

        if not payload:
            return format_warning("No SSL settings to update")

        response = await make_api_request(
            method="PATCH",
            endpoint=f"/sites/{site_id}/maindomain",
            json_data=payload,
            username=username,
            password=password
        )
        domain_info = response.get("domain", response.get("data", response))

        return format_success(
            "Main domain SSL settings updated",
            {
                "site_id": site_id,
                "domain": domain_info.get("domain"),
                "validation_method": domain_info.get("validation_method"),
                "ssl_ca": domain_info.get("ssl_ca"),
                "ssl_status": domain_info.get("ssl_status"),
                "ssl_renewal_date": domain_info.get("ssl_renewal_date")
            }
        )

    except Exception as e:
        return format_error(f"Failed to update SSL settings: {str(e)}")


async def get_domain_edge_settings(
    site_id: str,
    domain_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get edge settings for an additional domain.

    Args:
        site_id: The ID of the site
        domain_id: The ID of the domain
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Edge settings for the domain
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/domains/{domain_id}/edge_settings",
            username=username,
            password=password
        )
        settings = response.get("edge_settings", response.get("data", response))

        return format_success(
            "Edge settings retrieved",
            {
                "domain_id": domain_id,
                "site_id": site_id,
                "cache_level": settings.get("cache_level"),
                "browser_cache_ttl": settings.get("browser_cache_ttl"),
                "always_online": settings.get("always_online"),
                "development_mode": settings.get("development_mode"),
                "minify": settings.get("minify"),
                "brotli": settings.get("brotli"),
                "auto_minify": settings.get("auto_minify"),
                "ssl_mode": settings.get("ssl_mode")
            }
        )

    except Exception as e:
        return format_error(f"Failed to get edge settings for domain {domain_id}: {str(e)}")


async def update_domain_edge_settings(
    site_id: str,
    domain_id: str,
    cache_level: Optional[str] = None,
    browser_cache_ttl: Optional[int] = None,
    always_online: Optional[bool] = None,
    development_mode: Optional[bool] = None,
    ssl_mode: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update edge settings for an additional domain.

    Args:
        site_id: The ID of the site
        domain_id: The ID of the domain
        cache_level: Cache level ("bypass", "basic", "standard", "aggressive")
        browser_cache_ttl: Browser cache TTL in seconds
        always_online: Enable always online feature
        development_mode: Enable development mode
        ssl_mode: SSL mode ("off", "flexible", "full", "full_strict")
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Updated edge settings
    """
    try:
        payload = {}

        if cache_level:
            payload["cache_level"] = cache_level
        if browser_cache_ttl is not None:
            payload["browser_cache_ttl"] = browser_cache_ttl
        if always_online is not None:
            payload["always_online"] = always_online
        if development_mode is not None:
            payload["development_mode"] = development_mode
        if ssl_mode:
            payload["ssl_mode"] = ssl_mode

        if not payload:
            return format_warning("No edge settings to update")

        response = await make_api_request(
            method="PATCH",
            endpoint=f"/sites/{site_id}/domains/{domain_id}/edge_settings",
            json_data=payload,
            username=username,
            password=password
        )
        settings = response.get("edge_settings", response.get("data", response))

        return format_success(
            "Edge settings updated",
            {
                "domain_id": domain_id,
                "site_id": site_id,
                "updated_settings": payload,
                "cache_cleared": settings.get("cache_cleared", False)
            }
        )

    except Exception as e:
        return format_error(f"Failed to update edge settings for domain {domain_id}: {str(e)}")