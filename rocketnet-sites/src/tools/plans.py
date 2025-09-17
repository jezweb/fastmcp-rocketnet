"""
Hosting Plan Tools for Rocket.net
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add parent directory to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from rocketnet_shared import (
    Config,
    RocketnetClient,
    format_success,
    format_error,
    format_warning,
)


async def list_plans(
    plan_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all available hosting plans.

    Args:
        plan_type: Filter by plan type (wordpress, agency, enterprise)

    Returns:
        List of available plans with their features
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            params = {}
            if plan_type:
                params["type"] = plan_type

            response = await client.get("/plans", params=params)
            plans = response.get("plans", response.get("data", []))

            formatted_plans = []
            for plan in plans:
                formatted_plans.append({
                    "id": plan.get("id"),
                    "name": plan.get("name"),
                    "type": plan.get("type"),
                    "price_monthly": plan.get("price_monthly"),
                    "price_annual": plan.get("price_annual"),
                    "features": {
                        "sites": plan.get("sites", 1),
                        "storage": plan.get("storage"),
                        "bandwidth": plan.get("bandwidth"),
                        "visits_monthly": plan.get("visits_monthly"),
                        "cdn_included": plan.get("cdn_included", True),
                        "ssl_included": plan.get("ssl_included", True),
                        "backups": plan.get("backups"),
                        "staging_sites": plan.get("staging_sites"),
                        "team_members": plan.get("team_members"),
                        "priority_support": plan.get("priority_support", False),
                        "white_label": plan.get("white_label", False),
                    },
                    "recommended_for": plan.get("recommended_for", [])
                })

            return format_success(
                f"Found {len(formatted_plans)} plans",
                {
                    "plans": formatted_plans,
                    "count": len(formatted_plans)
                }
            )

    except Exception as e:
        return format_error(f"Failed to list plans: {str(e)}")


async def get_plan_details(plan_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific hosting plan.

    Args:
        plan_id: The ID of the plan (starter, pro, business, agency, etc.)

    Returns:
        Detailed plan information including all features
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            response = await client.get(f"/plans/{plan_id}")
            plan = response.get("plan", response.get("data", response))

            return format_success(
                f"Plan details for {plan.get('name', plan_id)}",
                {
                    "id": plan.get("id"),
                    "name": plan.get("name"),
                    "type": plan.get("type"),
                    "description": plan.get("description"),
                    "price": {
                        "monthly": plan.get("price_monthly"),
                        "annual": plan.get("price_annual"),
                        "currency": plan.get("currency", "USD"),
                        "savings_annual": plan.get("savings_annual")
                    },
                    "features": {
                        "sites": plan.get("sites"),
                        "storage": plan.get("storage"),
                        "bandwidth": plan.get("bandwidth"),
                        "visits_monthly": plan.get("visits_monthly"),
                        "cdn": {
                            "included": plan.get("cdn_included", True),
                            "locations": plan.get("cdn_locations")
                        },
                        "ssl": {
                            "included": plan.get("ssl_included", True),
                            "wildcard": plan.get("ssl_wildcard", False)
                        },
                        "backups": {
                            "frequency": plan.get("backup_frequency"),
                            "retention": plan.get("backup_retention"),
                            "on_demand": plan.get("backup_on_demand", True)
                        },
                        "staging": {
                            "sites": plan.get("staging_sites"),
                            "push_to_live": plan.get("staging_push_to_live", True)
                        },
                        "team": {
                            "members": plan.get("team_members"),
                            "roles": plan.get("team_roles", [])
                        },
                        "support": {
                            "level": plan.get("support_level"),
                            "priority": plan.get("priority_support", False),
                            "phone": plan.get("phone_support", False),
                            "response_time": plan.get("support_response_time")
                        },
                        "developer": {
                            "ssh_access": plan.get("ssh_access", True),
                            "git_integration": plan.get("git_integration", False),
                            "wp_cli": plan.get("wp_cli", True),
                            "php_versions": plan.get("php_versions", [])
                        }
                    },
                    "limits": plan.get("limits", {}),
                    "addons": plan.get("available_addons", [])
                }
            )

    except Exception as e:
        return format_error(f"Failed to get plan {plan_id}: {str(e)}")


async def change_site_plan(
    site_id: str,
    new_plan_id: str,
    confirm: bool = False
) -> Dict[str, Any]:
    """
    Change the hosting plan for a site.

    Args:
        site_id: The ID of the site to update
        new_plan_id: The ID of the new plan
        confirm: Must be True to confirm the plan change

    Returns:
        Information about the plan change
    """
    try:
        if not confirm:
            return format_warning(
                "Plan change requires confirmation",
                {
                    "message": "Set confirm=True to change the plan. This may affect billing.",
                    "site_id": site_id,
                    "new_plan": new_plan_id
                }
            )

        config = Config.from_env()
        async with RocketnetClient(config) as client:
            # Get current site info
            site_response = await client.get(f"/sites/{site_id}")
            site = site_response.get("site", site_response.get("data", {}))
            current_plan = site.get("plan")

            # Change the plan
            payload = {"plan": new_plan_id}
            response = await client.patch(f"/sites/{site_id}/plan", payload)

            result = response.get("result", response.get("data", response))

            return format_success(
                f"Plan changed from {current_plan} to {new_plan_id}",
                {
                    "site_id": site_id,
                    "site_name": site.get("name"),
                    "previous_plan": current_plan,
                    "new_plan": new_plan_id,
                    "effective_date": result.get("effective_date"),
                    "prorated_amount": result.get("prorated_amount"),
                    "next_billing_amount": result.get("next_billing_amount"),
                    "status": result.get("status", "Plan change in progress")
                }
            )

    except Exception as e:
        return format_error(f"Failed to change plan for site {site_id}: {str(e)}")