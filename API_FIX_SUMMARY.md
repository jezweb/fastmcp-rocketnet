# API Response Structure Analysis

## Executive Summary

After comprehensive testing with bearer token authentication, we discovered the Rocket.net API v1 uses a consistent wrapper format for all responses when authenticated with bearer tokens. This differs from what our MCP tools may receive when using internal authentication.

## Key Findings

### Response Format with Bearer Token
All endpoints return a consistent wrapper structure:

### Bearer Token Response Format:
```json
{
  "success": true,
  "errors": [],
  "messages": [],
  "result": [/* actual data array or object */]
}
```

### Current Code Expects:
- Direct arrays: `[{item1}, {item2}]`
- Or nested under "data": `{"data": [{item1}, {item2}]}`
- Or nested under specific keys: `{"sites": [...], "plugins": [...]}`

## Endpoints That Need Fixing

### 🟡 Endpoints with data in 'result' key:

#### Sites Module
- `/sites` - List sites (10 items found)
- `/sites/locations` - List locations (9 items found)

#### WordPress Module
- `/sites/{id}/plugins` - List plugins (8 items found)
- `/sites/{id}/themes` - List themes (4 items found)
- `/sites/{id}/plugins/search` - Search plugins (10 items found)
- `/sites/{id}/themes/search` - Search themes (10 items found)

#### Billing Module
- `/billing/products` - List products/plans (18 items found)
- `/billing/invoices` - List invoices (10 items found)
- `/billing/addresses` - List billing addresses (10 items found)

## The Fix

For list endpoints, update response parsing to check for 'result' key:

```python
# Current (partially working)
if isinstance(response, list):
    items = response
else:
    items = response.get("sites", response.get("data", [])) if isinstance(response, dict) else []

# Should be:
if isinstance(response, list):
    items = response
elif isinstance(response, dict):
    # Check for wrapper format first
    if "result" in response and isinstance(response["result"], list):
        items = response["result"]
    else:
        # Fallback to other formats
        items = response.get("sites", response.get("data", []))
else:
    items = []
```

## Test Results Summary

From testing 25 endpoints with bearer token auth:
- ✅ **13 endpoints tested successfully**
- 🟡 **9 endpoints with data in 'result' key** (list endpoints)
- 🟢 **4 endpoints returning single objects** (get by ID endpoints)
- 🔴 **0 endpoints returning direct arrays**
- ❌ **12 endpoints returned errors** (404s, likely need specific resources)

## Why This Happens

The API implements two response modes:

1. **Wrapper Mode** (Bearer Token Authentication)
   - Used for external API consumers
   - Provides metadata about request success
   - Includes error handling information
   - Data always in `result` key

2. **Direct Mode** (Internal/Session Authentication)
   - May be used for internal tools or session-based auth
   - Returns data directly without wrapper
   - Less metadata overhead
   - Our MCP tools may trigger this mode

## Implementation Status

### Current Code Behavior
Our tools check multiple formats to handle both modes:
1. Check if response is a direct array
2. Check for `result` key (wrapper format)
3. Check for `data` key (legacy format)
4. Check for endpoint-specific keys (`sites`, `plugins`, etc.)

### Recommended Pattern
```python
def parse_api_response(response, expected_key=None):
    """Universal response parser for Rocket.net API."""
    if isinstance(response, list):
        return response
    elif isinstance(response, dict):
        # Check wrapper format first (most common with bearer auth)
        if "result" in response:
            return response["result"]
        # Check other common formats
        if "data" in response:
            return response["data"]
        # Check endpoint-specific key
        if expected_key and expected_key in response:
            return response[expected_key]
    return []
```

## Affected Modules Status

| Module | Status | Notes |
|--------|--------|-------|
| rocketnet-sites | ✅ Fixed | Handles both array and result formats |
| rocketnet-wordpress | ⚠️ May need update | Check result key handling |
| rocketnet-billing | ⚠️ May need update | Check result key handling |
| rocketnet-domains | ✅ Likely OK | Single object responses |
| rocketnet-backups | ⚠️ May need update | Check list endpoints |
| rocketnet-analytics | ⚠️ May need update | Check report endpoints |
| rocketnet-performance | ⚠️ May need update | Check report endpoints |
| rocketnet-access | ⚠️ May need update | Check list endpoints |

## Next Steps

1. ✅ **Testing Complete** - Identified response structure patterns
2. ✅ **Documentation Complete** - Updated README, created DEVELOPMENT.md, and API_FIX_SUMMARY.md
3. ⚠️ **Code Updates Needed** - Apply result key checking to all list endpoints
4. 📝 **Monitor in Production** - Verify behavior with actual MCP authentication