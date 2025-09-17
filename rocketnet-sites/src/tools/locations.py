"""
Data Center Location Tools for Rocket.net
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add parent directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import make_api_request
from utils import format_success, format_error


async def list_locations() -> Dict[str, Any]:
    """
    List all available data center locations for Rocket.net sites.

    Returns:
        List of available locations with their details
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint="/sites/locations"
        )
        locations = response.get("locations", response.get("data", []))

        formatted_locations = []
        for loc in locations:
            formatted_locations.append({
                "id": loc.get("id"),
                "name": loc.get("name"),
                "region": loc.get("region"),
                "country": loc.get("country"),
                "city": loc.get("city"),
                "available": loc.get("available", True),
                "features": loc.get("features", []),
                "latency_info": loc.get("latency_info"),
            })

        return format_success(
            f"Found {len(formatted_locations)} locations",
            {
                "locations": formatted_locations,
                "count": len(formatted_locations),
                "recommended": next(
                    (loc for loc in formatted_locations if loc.get("recommended")),
                    formatted_locations[0] if formatted_locations else None
                )
            }
        )

    except Exception as e:
        return format_error(f"Failed to list locations: {str(e)}")


async def get_location_info(location_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific data center location.

    Args:
        location_id: The ID of the location

    Returns:
        Detailed location information
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/locations/{location_id}"
        )
        location = response.get("location", response.get("data", response))

        return format_success(
            f"Location details for {location.get('name', location_id)}",
            {
                "id": location.get("id"),
                "name": location.get("name"),
                "region": location.get("region"),
                "country": location.get("country"),
                "city": location.get("city"),
                "available": location.get("available", True),
                "features": location.get("features", []),
                "cdn_coverage": location.get("cdn_coverage"),
                "backup_locations": location.get("backup_locations", []),
                "network_info": location.get("network_info"),
                "compliance": location.get("compliance", []),
                "status": location.get("status", "operational")
            }
        )

    except Exception as e:
        return format_error(f"Failed to get location {location_id}: {str(e)}")