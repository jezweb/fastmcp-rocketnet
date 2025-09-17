"""
Rocket.net Billing & Account Management MCP Server
===================================================
Invoice management, payment methods, and account administration.
"""

import os
import sys
from pathlib import Path

from fastmcp import FastMCP
from utils import format_success, format_error

# Import tools
from tools.billing import (
    list_invoices,
    get_invoice,
    download_invoice_pdf,
    list_payment_methods,
    add_payment_method,
    delete_payment_method,
    list_billing_addresses,
    get_account_usage,
    list_account_users,
    add_account_user,
    remove_account_user,
    get_available_products,
)

# Initialize FastMCP server - MUST be at module level for FastMCP Cloud
mcp = FastMCP(
    name="rocketnet-billing",
    instructions="""
    This server provides billing and account management tools for Rocket.net.

    Available tools:
    - list_invoices: View all account invoices
    - get_invoice: Get detailed invoice information
    - download_invoice_pdf: Generate PDF download link
    - list_payment_methods: View saved payment methods
    - add_payment_method: Add a new payment method
    - delete_payment_method: Remove a payment method
    - list_billing_addresses: View billing addresses
    - get_account_usage: Monitor resource usage and costs
    - list_account_users: View users with account access
    - add_account_user: Add a new user to the account
    - remove_account_user: Remove user access
    - get_available_products: View available plans and add-ons

    Billing Features:
    - Invoice management and downloads
    - Payment method management
    - Usage monitoring and cost analysis
    - User access control
    - Billing address management

    Resources:
    - billing://account/overview - Complete billing overview
    - account://users/all - All account users

    All operations require proper authentication via environment variables:
    ROCKETNET_EMAIL and ROCKETNET_PASSWORD
    """
)

# Register tools
mcp.tool(list_invoices)
mcp.tool(get_invoice)
mcp.tool(download_invoice_pdf)
mcp.tool(list_payment_methods)
mcp.tool(add_payment_method)
mcp.tool(delete_payment_method)
mcp.tool(list_billing_addresses)
mcp.tool(get_account_usage)
mcp.tool(list_account_users)
mcp.tool(add_account_user)
mcp.tool(remove_account_user)
mcp.tool(get_available_products)

# Register resources
@mcp.resource("billing://account/overview")
async def billing_overview_resource() -> str:
    """Get complete billing overview for the account."""
    try:
        from auth import make_api_request
        import json

        # Get recent invoices
        invoices_response = await make_api_request(
            "GET",
            "/billing/invoices",
            params={"limit": 5}
        )

        # Get account usage
        usage_response = await make_api_request(
            "GET",
            "/account/usage",
            params={"period": "current"}
        )

        overview = {
            "recent_invoices": invoices_response.get("invoices", [])[:5],
            "current_usage": usage_response.get("usage", {}),
            "timestamp": "current"
        }

        return json.dumps(overview, indent=2)
    except Exception as e:
        import json
        return json.dumps({"error": str(e)}, indent=2)

@mcp.resource("account://users/all")
async def account_users_resource() -> str:
    """Get all account users and their permissions."""
    try:
        from auth import make_api_request
        import json

        response = await make_api_request("GET", "/account/users")
        users = response.get("users", response.get("data", []))

        return json.dumps({
            "users": users,
            "total_users": len(users),
            "roles": {
                "owners": sum(1 for u in users if u.get("role") == "owner"),
                "admins": sum(1 for u in users if u.get("role") == "admin"),
                "users": sum(1 for u in users if u.get("role") == "user")
            }
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