"""
Billing and Account Management Tools for Rocket.net
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# Add parent directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import make_api_request
from utils import format_success, format_error, format_warning, format_datetime


async def list_invoices(
    status: Optional[str] = None,
    limit: int = 50,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all invoices for the account.

    Args:
        status: Filter by status (paid, unpaid, pending)
        limit: Maximum number of invoices to return
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of invoices with details
    """
    try:
        params = {"limit": limit}
        if status:
            params["status"] = status

        response = await make_api_request(
            method="GET",
            endpoint="/billing/invoices",
            params=params,
            username=username,
            password=password
        )
        invoices = response.get("invoices", response.get("data", []))

        formatted_invoices = []
        total_amount = 0

        for invoice in invoices[:limit]:
            amount = invoice.get("amount", 0)
            total_amount += amount if invoice.get("status") == "paid" else 0

            formatted_invoices.append({
                "invoice_id": invoice.get("id"),
                "invoice_number": invoice.get("number"),
                "date": format_datetime(invoice.get("date")),
                "due_date": format_datetime(invoice.get("due_date")),
                "amount": f"${amount:.2f}",
                "status": invoice.get("status"),
                "description": invoice.get("description"),
                "pdf_url": invoice.get("pdf_url")
            })

        return format_success(
            f"Found {len(formatted_invoices)} invoices",
            {
                "invoices": formatted_invoices,
                "count": len(formatted_invoices),
                "total_paid": f"${total_amount:.2f}",
                "unpaid_count": sum(1 for i in formatted_invoices if i["status"] == "unpaid")
            }
        )

    except Exception as e:
        return format_error(f"Failed to list invoices: {str(e)}")


async def get_invoice(
    invoice_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get details of a specific invoice.

    Args:
        invoice_id: The ID of the invoice
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Detailed invoice information
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/billing/invoices/{invoice_id}",
            username=username,
            password=password
        )
        invoice = response.get("invoice", response.get("data", response))

        line_items = []
        for item in invoice.get("line_items", []):
            line_items.append({
                "description": item.get("description"),
                "quantity": item.get("quantity"),
                "unit_price": f"${item.get('unit_price', 0):.2f}",
                "total": f"${item.get('total', 0):.2f}"
            })

        return format_success(
            f"Invoice {invoice.get('number')} retrieved",
            {
                "invoice_id": invoice.get("id"),
                "invoice_number": invoice.get("number"),
                "date": format_datetime(invoice.get("date")),
                "due_date": format_datetime(invoice.get("due_date")),
                "amount": f"${invoice.get('amount', 0):.2f}",
                "tax": f"${invoice.get('tax', 0):.2f}",
                "total": f"${invoice.get('total', 0):.2f}",
                "status": invoice.get("status"),
                "line_items": line_items,
                "payment_method": invoice.get("payment_method"),
                "pdf_url": invoice.get("pdf_url")
            }
        )

    except Exception as e:
        return format_error(f"Failed to get invoice {invoice_id}: {str(e)}")


async def download_invoice_pdf(
    invoice_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get download URL for invoice PDF.

    Args:
        invoice_id: The ID of the invoice
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        PDF download URL
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/billing/invoices/{invoice_id}/pdf",
            username=username,
            password=password
        )
        pdf_info = response.get("pdf", response.get("data", response))

        return format_success(
            "Invoice PDF URL generated",
            {
                "invoice_id": invoice_id,
                "pdf_url": pdf_info.get("url"),
                "expires_at": format_datetime(pdf_info.get("expires_at")),
                "filename": pdf_info.get("filename")
            }
        )

    except Exception as e:
        return format_error(f"Failed to get invoice PDF: {str(e)}")


async def list_payment_methods(
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all payment methods on the account.

    Args:
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of payment methods
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint="/billing/payment-methods",
            username=username,
            password=password
        )
        methods = response.get("payment_methods", response.get("data", []))

        formatted_methods = []
        for method in methods:
            formatted_methods.append({
                "id": method.get("id"),
                "type": method.get("type"),
                "brand": method.get("brand"),
                "last4": method.get("last4"),
                "exp_month": method.get("exp_month"),
                "exp_year": method.get("exp_year"),
                "is_default": method.get("is_default", False),
                "created_at": format_datetime(method.get("created_at"))
            })

        default_method = next((m for m in formatted_methods if m["is_default"]), None)

        return format_success(
            f"Found {len(formatted_methods)} payment methods",
            {
                "payment_methods": formatted_methods,
                "count": len(formatted_methods),
                "default_method": default_method
            }
        )

    except Exception as e:
        return format_error(f"Failed to list payment methods: {str(e)}")


async def add_payment_method(
    payment_token: str,
    set_as_default: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a new payment method to the account.

    Args:
        payment_token: Payment token from payment processor
        set_as_default: Set this as the default payment method
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the added payment method
    """
    try:
        payload = {
            "token": payment_token,
            "set_default": set_as_default
        }

        response = await make_api_request(
            method="POST",
            endpoint="/billing/payment-methods",
            json_data=payload,
            username=username,
            password=password
        )
        method = response.get("payment_method", response.get("data", response))

        return format_success(
            "Payment method added successfully",
            {
                "payment_method_id": method.get("id"),
                "type": method.get("type"),
                "brand": method.get("brand"),
                "last4": method.get("last4"),
                "is_default": method.get("is_default", set_as_default)
            }
        )

    except Exception as e:
        return format_error(f"Failed to add payment method: {str(e)}")


async def delete_payment_method(
    payment_method_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove a payment method from the account.

    Args:
        payment_method_id: The ID of the payment method to remove
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of payment method removal
    """
    try:
        await make_api_request(
            method="DELETE",
            endpoint=f"/billing/payment-methods/{payment_method_id}",
            username=username,
            password=password
        )

        return format_success(
            "Payment method removed successfully",
            {
                "removed_payment_method_id": payment_method_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to remove payment method: {str(e)}")


async def list_billing_addresses(
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all billing addresses on the account.

    Args:
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of billing addresses
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint="/billing/addresses",
            username=username,
            password=password
        )
        addresses = response.get("addresses", response.get("data", []))

        formatted_addresses = []
        for address in addresses:
            formatted_addresses.append({
                "id": address.get("id"),
                "name": address.get("name"),
                "company": address.get("company"),
                "address_line1": address.get("line1"),
                "address_line2": address.get("line2"),
                "city": address.get("city"),
                "state": address.get("state"),
                "postal_code": address.get("postal_code"),
                "country": address.get("country"),
                "is_default": address.get("is_default", False)
            })

        return format_success(
            f"Found {len(formatted_addresses)} billing addresses",
            {
                "addresses": formatted_addresses,
                "count": len(formatted_addresses),
                "default_address": next((a for a in formatted_addresses if a["is_default"]), None)
            }
        )

    except Exception as e:
        return format_error(f"Failed to list billing addresses: {str(e)}")


async def get_account_usage(
    period: str = "current",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get account usage statistics and costs.

    Args:
        period: Billing period (current, previous, year)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Account usage and cost breakdown
    """
    try:
        params = {"period": period}

        response = await make_api_request(
            method="GET",
            endpoint="/account/usage",
            params=params,
            username=username,
            password=password
        )
        usage = response.get("usage", response.get("data", response))

        return format_success(
            f"Account usage for {period} period",
            {
                "period": period,
                "period_start": format_datetime(usage.get("period_start")),
                "period_end": format_datetime(usage.get("period_end")),
                "sites": {
                    "total": usage.get("total_sites", 0),
                    "active": usage.get("active_sites", 0),
                    "staging": usage.get("staging_sites", 0)
                },
                "resources": {
                    "total_bandwidth_gb": usage.get("bandwidth_gb", 0),
                    "total_storage_gb": usage.get("storage_gb", 0),
                    "total_compute_hours": usage.get("compute_hours", 0),
                    "cdn_requests": usage.get("cdn_requests", 0)
                },
                "costs": {
                    "hosting": f"${usage.get('hosting_cost', 0):.2f}",
                    "overages": f"${usage.get('overage_cost', 0):.2f}",
                    "add_ons": f"${usage.get('addon_cost', 0):.2f}",
                    "total": f"${usage.get('total_cost', 0):.2f}",
                    "projected_monthly": f"${usage.get('projected_monthly', 0):.2f}"
                }
            }
        )

    except Exception as e:
        return format_error(f"Failed to get account usage: {str(e)}")


async def list_account_users(
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all users with access to the account.

    Args:
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of account users and their permissions
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint="/account/users",
            username=username,
            password=password
        )
        users = response.get("users", response.get("data", []))

        formatted_users = []
        for user in users:
            formatted_users.append({
                "user_id": user.get("id"),
                "email": user.get("email"),
                "name": user.get("name"),
                "role": user.get("role"),
                "status": user.get("status"),
                "created_at": format_datetime(user.get("created_at")),
                "last_login": format_datetime(user.get("last_login")),
                "permissions": user.get("permissions", [])
            })

        return format_success(
            f"Found {len(formatted_users)} account users",
            {
                "users": formatted_users,
                "count": len(formatted_users),
                "owner_count": sum(1 for u in formatted_users if u["role"] == "owner"),
                "admin_count": sum(1 for u in formatted_users if u["role"] == "admin"),
                "user_count": sum(1 for u in formatted_users if u["role"] == "user")
            }
        )

    except Exception as e:
        return format_error(f"Failed to list account users: {str(e)}")


async def add_account_user(
    email: str,
    role: str = "user",
    site_access: Optional[List[str]] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a new user to the account.

    Args:
        email: Email address of the new user
        role: User role (owner, admin, user)
        site_access: List of site IDs the user can access
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the added user
    """
    try:
        payload = {
            "email": email,
            "role": role
        }

        if site_access:
            payload["site_access"] = site_access

        response = await make_api_request(
            method="POST",
            endpoint="/account/users",
            json_data=payload,
            username=username,
            password=password
        )
        user = response.get("user", response.get("data", response))

        return format_success(
            f"User {email} added to account",
            {
                "user_id": user.get("id"),
                "email": email,
                "role": role,
                "invite_sent": user.get("invite_sent", True),
                "invite_expires": format_datetime(user.get("invite_expires"))
            }
        )

    except Exception as e:
        return format_error(f"Failed to add user {email}: {str(e)}")


async def remove_account_user(
    user_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove a user from the account.

    Args:
        user_id: The ID of the user to remove
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of user removal
    """
    try:
        await make_api_request(
            method="DELETE",
            endpoint=f"/account/users/{user_id}",
            username=username,
            password=password
        )

        return format_success(
            "User removed from account",
            {
                "removed_user_id": user_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to remove user {user_id}: {str(e)}")


async def get_available_products(
    category: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List available products and add-ons.

    Args:
        category: Filter by category (hosting, addon, feature)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of available products
    """
    try:
        params = {}
        if category:
            params["category"] = category

        response = await make_api_request(
            method="GET",
            endpoint="/billing/products",
            params=params,
            username=username,
            password=password
        )
        products = response.get("products", response.get("data", []))

        formatted_products = []
        for product in products:
            formatted_products.append({
                "product_id": product.get("id"),
                "name": product.get("name"),
                "category": product.get("category"),
                "price": f"${product.get('price', 0):.2f}",
                "billing_cycle": product.get("billing_cycle"),
                "description": product.get("description"),
                "features": product.get("features", []),
                "limits": product.get("limits", {})
            })

        return format_success(
            f"Found {len(formatted_products)} available products",
            {
                "products": formatted_products,
                "count": len(formatted_products),
                "categories": list(set(p["category"] for p in formatted_products))
            }
        )

    except Exception as e:
        return format_error(f"Failed to get available products: {str(e)}")