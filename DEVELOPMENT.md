# Development Guide

## Architecture Overview

This project consists of 8 independent MCP servers, each handling specific Rocket.net API domains. Each server is self-contained to enable independent deployment to FastMCP Cloud.

## Core Components

### Authentication Module (`auth.py`)

Each server has its own authentication module that:
1. Accepts username/password (from params or environment)
2. Calls `/login` endpoint to get JWT token
3. Adds `Bearer {token}` to all API requests
4. Handles token refresh automatically

```python
# The authentication flow
async def make_api_request(
    method: str,
    endpoint: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    ...
):
    # Get auth headers (handles login automatically)
    headers = await get_auth_headers(username, password)
    # Make the API request with bearer token
    response = await client.request(...)
```

### Response Parsing

Due to API response format variations, all list endpoints use this pattern:

```python
# Handle multiple response formats
if isinstance(response, list):
    # Direct array response
    items = response
elif isinstance(response, dict):
    # Check for wrapper format first (bearer token auth)
    if "result" in response:
        items = response["result"]
    else:
        # Check for other nested formats
        items = response.get("expected_key", response.get("data", []))
else:
    items = []
```

### Utility Functions (`utils.py`)

Common formatting functions across all servers:
- `format_success()` - Consistent success responses
- `format_error()` - Error handling
- `format_warning()` - Warning messages
- `format_datetime()` - Date formatting
- `format_size()` - Byte size formatting

## API Response Formats

### Discovery Process

Through testing with bearer tokens, we discovered the API has two response modes:

1. **Wrapper Mode** (Bearer Token Auth)
   ```json
   {
     "success": true,
     "errors": [],
     "messages": [],
     "metadata": {...},
     "result": [...]  // Actual data here
   }
   ```

2. **Direct Mode** (Internal/Tool Auth)
   ```json
   [
     {"id": 1, "name": "Item 1"},
     {"id": 2, "name": "Item 2"}
   ]
   ```

### Testing Response Formats

Use the provided test script to verify endpoint responses:

```bash
# Setup
cp .env.template .env
# Add your ROCKETNET_BEARER_TOKEN to .env

# Run tests
python test_api_endpoints.py
```

The script will show:
- 🟡 Yellow: Data in `result` key (wrapper format)
- 🟢 Green: Direct object response
- 🔴 Red: Direct array response

## Adding New Tools

### 1. Identify the API Endpoint

Check the [Rocket.net API docs](https://rocketdotnet.readme.io/reference/) or `api-endpoints.md` for available endpoints.

### 2. Create Tool Function

```python
async def new_tool(
    site_id: str,
    param1: Optional[str] = None,
    username: Optional[str] = None,  # Always include
    password: Optional[str] = None   # Always include
) -> Dict[str, Any]:
    """
    Tool description.

    Args:
        site_id: The site ID
        param1: Description
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Formatted response with data
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/endpoint",
            username=username,
            password=password
        )

        # Parse response based on type
        if isinstance(response, list):
            items = response
        elif isinstance(response, dict):
            if "result" in response:
                items = response["result"]
            else:
                items = response.get("data", [])
        else:
            items = []

        return format_success(
            f"Found {len(items)} items",
            {"items": items, "count": len(items)}
        )

    except Exception as e:
        return format_error(f"Failed to fetch data: {str(e)}")
```

### 3. Register Tool

In `server.py`:

```python
from tools.module import new_tool

# Register with FastMCP
mcp.tool(new_tool)
```

## Common Patterns

### List Endpoints

Most list endpoints follow this pattern:
1. Optional filters (status, type, etc.)
2. Return array of items
3. Handle pagination if supported

### Action Endpoints

Actions typically:
1. Accept resource ID
2. Perform operation (POST/PUT/PATCH/DELETE)
3. Return confirmation with updated state

### Resource-Specific Patterns

- **Sites**: Most endpoints require `site_id`
- **Billing**: Account-level, no site_id needed
- **WordPress**: Require site_id, may need plugin/theme slug
- **Domains**: Require site_id, may need domain_id

## Testing

### Manual Testing

```bash
# Run server locally
cd rocketnet-sites
fastmcp dev src/server.py

# Test with Claude Desktop or MCP client
```

### API Testing

```python
# Test individual endpoints
import asyncio
from tools.sites import list_sites

async def test():
    result = await list_sites(
        username="test@example.com",
        password="testpass"
    )
    print(result)

asyncio.run(test())
```

## Debugging

### Enable Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

1. **Empty Results**: Check if data is in `result` key
2. **Auth Errors**: Verify credentials and token generation
3. **404 Errors**: Check endpoint path and parameters
4. **Rate Limits**: Add retry logic with backoff

## Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
fastmcp dev src/server.py
```

### FastMCP Cloud

1. Push changes to GitHub
2. FastMCP Cloud auto-deploys from main branch
3. Monitor logs in FastMCP Cloud dashboard

## Contributing

1. Test changes locally first
2. Update relevant documentation
3. Ensure auth parameters are included
4. Handle all response formats
5. Add error handling
6. Create PR with clear description

## Resources

- [Rocket.net API Documentation](https://rocketdotnet.readme.io/reference/)
- [FastMCP Documentation](https://docs.fastmcp.com/)
- [MCP Specification](https://modelcontextprotocol.io/)
- `api-endpoints.md` - Complete endpoint list
- `test_api_endpoints.py` - Response format tester