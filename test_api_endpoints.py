#!/usr/bin/env python3
"""
Test Rocket.net API endpoints to determine response structure.
This helps identify which endpoints return arrays vs objects.
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any, Optional, List
import httpx
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
API_BASE = "https://api.rocket.net/v1"
BEARER_TOKEN = os.getenv("ROCKETNET_BEARER_TOKEN")
SITE_ID = os.getenv("ROCKETNET_SITE_ID")
BACKUP_ID = os.getenv("ROCKETNET_BACKUP_ID")
DOMAIN_ID = os.getenv("ROCKETNET_DOMAIN_ID")
INVOICE_ID = os.getenv("ROCKETNET_INVOICE_ID")

if not BEARER_TOKEN:
    print("❌ Error: ROCKETNET_BEARER_TOKEN not found in .env file")
    print("Please copy .env.template to .env and add your bearer token")
    sys.exit(1)

# Test results storage
test_results = []

# Define all endpoints to test
ENDPOINTS = [
    # Sites endpoints
    {"method": "GET", "endpoint": "/sites", "name": "List sites", "category": "Sites"},
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}", "name": "Get site", "category": "Sites", "requires": "SITE_ID"},
    {"method": "GET", "endpoint": "/sites/locations", "name": "List locations", "category": "Sites"},
    {"method": "GET", "endpoint": "/sites/templates", "name": "List templates", "category": "Sites"},

    # WordPress endpoints
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/plugins", "name": "List plugins", "category": "WordPress", "requires": "SITE_ID"},
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/themes", "name": "List themes", "category": "WordPress", "requires": "SITE_ID"},
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/plugins/search?search=contact", "name": "Search plugins", "category": "WordPress", "requires": "SITE_ID"},
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/themes/search?search=twenty", "name": "Search themes", "category": "WordPress", "requires": "SITE_ID"},

    # Access endpoints
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/ssh-keys", "name": "List SSH keys", "category": "Access", "requires": "SITE_ID"},
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/ftp-accounts", "name": "List FTP accounts", "category": "Access", "requires": "SITE_ID"},
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/file-manager/files?path=/", "name": "List files", "category": "Access", "requires": "SITE_ID"},
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/password-protection/users", "name": "List protected users", "category": "Access", "requires": "SITE_ID"},

    # Billing endpoints
    {"method": "GET", "endpoint": "/billing/products", "name": "List products/plans", "category": "Billing"},
    {"method": "GET", "endpoint": "/billing/invoices", "name": "List invoices", "category": "Billing"},
    {"method": "GET", "endpoint": "/billing/payment-methods", "name": "List payment methods", "category": "Billing"},
    {"method": "GET", "endpoint": "/billing/addresses", "name": "List billing addresses", "category": "Billing"},

    # Account endpoints
    {"method": "GET", "endpoint": "/account/users", "name": "List account users", "category": "Account"},
    {"method": "GET", "endpoint": "/account/visitors", "name": "Get visitor stats", "category": "Account"},
    {"method": "GET", "endpoint": "/account/usage", "name": "Get usage stats", "category": "Account"},

    # Domain endpoints
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/domains", "name": "List domains", "category": "Domains", "requires": "SITE_ID"},
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/maindomain", "name": "Get main domain", "category": "Domains", "requires": "SITE_ID"},

    # Backup endpoints
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/backups", "name": "List backups", "category": "Backups", "requires": "SITE_ID"},
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/cloud-backups", "name": "List cloud backups", "category": "Backups", "requires": "SITE_ID"},

    # Analytics endpoints
    {"method": "GET", "endpoint": f"/sites/{SITE_ID}/access-logs", "name": "List access logs", "category": "Analytics", "requires": "SITE_ID"},
    {"method": "GET", "endpoint": f"/reporting/sites/{SITE_ID}/visitors", "name": "Visitor report", "category": "Analytics", "requires": "SITE_ID"},
]

async def test_endpoint(client: httpx.AsyncClient, endpoint_config: Dict[str, Any]) -> Dict[str, Any]:
    """Test a single endpoint and analyze its response structure."""

    # Skip if required variable is missing
    if endpoint_config.get("requires"):
        required_var = endpoint_config["requires"]
        if required_var == "SITE_ID" and not SITE_ID:
            return {
                **endpoint_config,
                "status": "SKIPPED",
                "reason": "SITE_ID not provided",
                "response_type": None,
                "is_array": None
            }

    try:
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        url = f"{API_BASE}{endpoint_config['endpoint']}"
        response = await client.request(
            method=endpoint_config["method"],
            url=url,
            headers=headers,
            timeout=10.0
        )

        if response.status_code == 200:
            try:
                data = response.json()

                # Analyze response structure
                is_array = isinstance(data, list)
                response_type = "array" if is_array else "object"

                # For objects, check what keys it has
                top_keys = []
                potential_array_keys = []
                actual_data_location = None
                if isinstance(data, dict):
                    top_keys = list(data.keys())[:5]  # First 5 keys
                    # Check for keys that contain arrays
                    for key, value in data.items():
                        if isinstance(value, list):
                            potential_array_keys.append(key)
                            # Check if this is the main data array
                            if key == "result":
                                actual_data_location = "result"
                            elif key == "data":
                                actual_data_location = "data"

                result = {
                    **endpoint_config,
                    "status": "SUCCESS",
                    "status_code": response.status_code,
                    "response_type": response_type,
                    "is_array": is_array,
                    "top_keys": top_keys if not is_array else None,
                    "array_keys": potential_array_keys if potential_array_keys else None,
                    "data_location": actual_data_location,
                    "sample_count": len(data) if is_array else len(data.get(actual_data_location, [])) if actual_data_location else None
                }

                # Print immediate feedback
                emoji = "🔴" if is_array else "🟡" if actual_data_location == "result" else "🟢"
                print(f"{emoji} {endpoint_config['name']}: {response_type}")
                if is_array:
                    print(f"   → Returns direct array with {len(data)} items")
                elif actual_data_location:
                    count = len(data.get(actual_data_location, []))
                    print(f"   → Data in '{actual_data_location}' key: {count} items")
                elif potential_array_keys:
                    print(f"   → Object with array keys: {', '.join(potential_array_keys)}")

                return result

            except json.JSONDecodeError:
                return {
                    **endpoint_config,
                    "status": "ERROR",
                    "status_code": response.status_code,
                    "error": "Invalid JSON response",
                    "response_type": None,
                    "is_array": None
                }
        else:
            return {
                **endpoint_config,
                "status": "HTTP_ERROR",
                "status_code": response.status_code,
                "error": f"HTTP {response.status_code}",
                "response_type": None,
                "is_array": None
            }

    except httpx.RequestError as e:
        return {
            **endpoint_config,
            "status": "NETWORK_ERROR",
            "error": str(e),
            "response_type": None,
            "is_array": None
        }

async def run_tests():
    """Run all endpoint tests."""
    print("=" * 60)
    print("🚀 Rocket.net API Endpoint Structure Test")
    print("=" * 60)
    print(f"API Base: {API_BASE}")
    print(f"Site ID: {SITE_ID if SITE_ID else 'Not provided'}")
    print(f"Total endpoints to test: {len(ENDPOINTS)}")
    print("=" * 60 + "\n")

    async with httpx.AsyncClient() as client:
        # Group by category for better output
        categories = {}
        for endpoint in ENDPOINTS:
            category = endpoint.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append(endpoint)

        # Test each category
        for category, endpoints in categories.items():
            print(f"\n📁 Testing {category} Endpoints")
            print("-" * 40)

            for endpoint in endpoints:
                result = await test_endpoint(client, endpoint)
                test_results.append(result)

    # Generate summary report
    print("\n" + "=" * 60)
    print("📊 SUMMARY REPORT")
    print("=" * 60)

    # Count results
    array_endpoints = [r for r in test_results if r.get("is_array") == True]
    object_endpoints = [r for r in test_results if r.get("is_array") == False]
    skipped = [r for r in test_results if r.get("status") == "SKIPPED"]
    errors = [r for r in test_results if r.get("status") in ["ERROR", "HTTP_ERROR", "NETWORK_ERROR"]]

    print(f"\n✅ Successfully tested: {len(array_endpoints) + len(object_endpoints)}")
    print(f"🔴 Direct arrays: {len(array_endpoints)}")
    print(f"🟢 Objects: {len(object_endpoints)}")
    print(f"⏭️  Skipped: {len(skipped)}")
    print(f"❌ Errors: {len(errors)}")

    if array_endpoints:
        print("\n🔴 Endpoints returning DIRECT ARRAYS (need fixing):")
        print("-" * 40)
        for r in array_endpoints:
            count = f" ({r['sample_count']} items)" if r.get('sample_count') is not None else ""
            print(f"  • {r['endpoint']}{count}")

    if object_endpoints:
        print("\n🟢 Endpoints returning OBJECTS (current code handles these):")
        print("-" * 40)
        for r in object_endpoints:
            keys_info = ""
            if r.get('array_keys'):
                keys_info = f" [arrays in: {', '.join(r['array_keys'])}]"
            print(f"  • {r['endpoint']}{keys_info}")

    # Save detailed report to file
    report_file = f"api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(test_results, f, indent=2, default=str)

    print(f"\n📄 Detailed report saved to: {report_file}")

    # Generate fixes needed
    if array_endpoints:
        print("\n🔧 FIXES NEEDED")
        print("=" * 60)
        print("The following files need array handling updates:\n")

        # Map endpoints to files
        fixes_needed = {}
        for r in array_endpoints:
            endpoint = r['endpoint']
            category = r.get('category', 'Unknown')

            # Map category to likely file
            file_map = {
                'Sites': 'rocketnet-sites/src/tools/sites.py',
                'WordPress': 'rocketnet-wordpress/src/tools/wordpress.py',
                'Access': 'rocketnet-access/src/tools/access.py',
                'Billing': 'rocketnet-billing/src/tools/billing.py',
                'Account': 'rocketnet-billing/src/tools/billing.py',
                'Domains': 'rocketnet-domains/src/tools/domains.py',
                'Backups': 'rocketnet-backups/src/tools/backups.py',
                'Analytics': 'rocketnet-analytics/src/tools/analytics.py',
            }

            file_path = file_map.get(category, 'Unknown')
            if file_path not in fixes_needed:
                fixes_needed[file_path] = []
            fixes_needed[file_path].append(endpoint)

        for file_path, endpoints in fixes_needed.items():
            print(f"\n📝 {file_path}:")
            for endpoint in endpoints:
                print(f"   • {endpoint}")

if __name__ == "__main__":
    asyncio.run(run_tests())