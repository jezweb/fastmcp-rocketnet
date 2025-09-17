# Rocket.net MCP Servers

A comprehensive collection of Model Context Protocol (MCP) servers for interacting with the Rocket.net hosting platform API. Built with FastMCP for easy deployment to FastMCP Cloud.

## Overview

This repository contains multiple specialized MCP servers that provide programmatic access to Rocket.net's hosting platform capabilities. Each server focuses on a specific domain of functionality, allowing for modular deployment and usage.

## Architecture

The project uses a modular multi-server approach where each server handles specific API endpoints:

- **rocketnet-sites** - Core site management and infrastructure
- **rocketnet-domains** - Domain and DNS management
- **rocketnet-backups** - Backup and recovery operations
- **rocketnet-performance** - CDN cache and performance monitoring

Each server is completely independent and self-contained for FastMCP Cloud compatibility.

## Quick Start

### Prerequisites

- Python 3.10+
- Rocket.net account credentials
- FastMCP installed (`pip install fastmcp`)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jezweb/fastmcp-rocketnet.git
cd fastmcp-rocketnet
```

2. Install server dependencies:
```bash
cd rocketnet-sites  # or any other server directory
pip install -r requirements.txt
```

3. Configure environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your Rocket.net credentials
```

4. Run a server locally:
```bash
fastmcp dev src/server.py
```

## Authentication

The servers support flexible authentication - you can either set environment variables once for personal use, or provide credentials with each tool call for shared/multi-tenant scenarios.

### Option 1: Environment Variables (Personal Use)

Set these once in your `.env` file or environment:

```env
ROCKETNET_USERNAME=your-email@example.com
ROCKETNET_PASSWORD=your-password
```

Then use tools without any auth parameters:
```python
result = await list_sites()
```

### Option 2: Direct Authentication (Shared Use)

Pass credentials directly with each tool call:

```python
result = await list_sites(
    username="your-email@example.com",
    password="your-password"
)
```

This approach is ideal for:
- Shared MCP servers
- Multi-tenant scenarios
- AI assistants that manage multiple accounts
- Situations where you don't want to store credentials

**Note:** The server automatically handles JWT token generation behind the scenes. You never need to manage tokens directly.

## Available Servers

### 1. Sites Management (`rocketnet-sites`)
Core site operations including creation, configuration, and monitoring.

**Key Tools:**
- `list_sites` - List all sites in your account
- `create_site` - Create a new WordPress site
- `get_site_status` - Check site health and status
- `update_site_settings` - Modify site configuration

### 2. Domain Management (`rocketnet-domains`)
Handle domains, DNS records, and SSL certificates.

**Key Tools:**
- `list_domains` - List all additional domains for a site
- `add_domain` - Add a domain alias to a site
- `get_main_domain` - Get main domain info and SSL status
- `set_main_domain` - Set the main domain for a site
- `update_domain_edge_settings` - Configure CDN/edge settings

### 3. Backup & Recovery (`rocketnet-backups`)
Comprehensive backup management and disaster recovery.

**Key Tools:**
- `create_backup` - Create manual backups
- `list_backups` - View all backups for a site
- `restore_backup` - Restore from backups
- `schedule_backup` - Configure automatic backups
- `download_backup` - Get backup download links

### 4. Performance & CDN (`rocketnet-performance`)
CDN cache management, bandwidth monitoring, and visitor analytics.

**Key Tools:**
- `purge_cache_files` - Clear specific cached files
- `purge_all_cache` - Clear entire site cache
- `get_cdn_requests_report` - View CDN traffic patterns
- `get_visitors_report` - Analyze visitor demographics
- `get_bandwidth_usage` - Monitor bandwidth consumption

## Deployment

### Local Development

Each server can be run independently:

```bash
# Run sites management server
cd rocketnet-sites
fastmcp dev src/server.py

# Run domains management server
cd rocketnet-domains
fastmcp dev src/server.py
```

### FastMCP Cloud Deployment

1. Push to GitHub
2. Connect repository at [fastmcp.cloud](https://fastmcp.cloud)
3. Configure environment variables
4. Deploy with one click

Each server can be deployed independently, allowing you to use only the functionality you need.

## Development

### Project Structure

```
fastmcp-rocketnet/
├── rocketnet-sites/        # Sites management server
├── rocketnet-domains/      # Domains server
├── rocketnet-backups/      # Backups server
├── rocketnet-performance/  # Performance server
├── README.md
├── SCRATCHPAD.md          # Development notes
└── DEPLOYMENT.md          # Deployment guide
```

Each server is self-contained with its own:
- `src/server.py` - FastMCP server definition
- `src/auth.py` - Authentication module
- `src/utils.py` - Utility functions
- `src/tools/` - Tool implementations
- `requirements.txt` - Python dependencies

### Testing

Run tests for individual servers:

```bash
cd rocketnet-sites
pytest tests/
```

## Usage Examples

### Using with Claude Desktop

Add servers to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "rocketnet-sites": {
      "command": "fastmcp",
      "args": ["dev", "/path/to/rocketnet-sites/src/server.py"],
      "env": {
        "ROCKETNET_EMAIL": "your-email@example.com",
        "ROCKETNET_PASSWORD": "your-password"
      }
    }
  }
}
```

### Example Interactions

```
Human: List all my Rocket.net sites
Assistant: I'll list all your Rocket.net sites for you.
[Uses list_sites tool]