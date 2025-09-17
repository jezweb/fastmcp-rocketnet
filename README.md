# Rocket.net MCP Servers

A comprehensive collection of Model Context Protocol (MCP) servers for interacting with the Rocket.net hosting platform API. Built with FastMCP for easy deployment to FastMCP Cloud.

## Overview

This repository contains multiple specialized MCP servers that provide programmatic access to Rocket.net's hosting platform capabilities. Each server focuses on a specific domain of functionality, allowing for modular deployment and usage.

## Architecture

The project uses a modular multi-server approach where each server handles specific API endpoints:

- **rocketnet-sites** - Core site management and infrastructure
- **rocketnet-domains** - Domain and DNS management
- **rocketnet-wordpress** - WordPress-specific operations
- **rocketnet-backups** - Backup and recovery operations
- **rocketnet-analytics** - Reporting and analytics
- **rocketnet-billing** - Billing and account management

All servers share common utilities through the `rocketnet-shared` package.

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

2. Install the shared package:
```bash
cd rocketnet-shared
pip install -e .
cd ..
```

3. Install server dependencies:
```bash
cd rocketnet-sites
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Rocket.net credentials
```

5. Run a server locally:
```bash
fastmcp dev src/server.py
```

## Configuration

Each server requires the following environment variables:

```env
ROCKETNET_EMAIL=your-email@example.com
ROCKETNET_PASSWORD=your-password
ROCKETNET_API_BASE=https://control.rocket.net/api  # Optional
```

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
- `add_domain` - Add a domain to a site
- `manage_dns` - Update DNS records
- `configure_ssl` - Manage SSL certificates

### 3. WordPress Management (`rocketnet-wordpress`)
WordPress-specific operations for plugins, themes, and updates.

**Key Tools:**
- `install_plugin` - Install WordPress plugins
- `update_themes` - Manage WordPress themes
- `create_staging` - Create staging environments

### 4. Backup & Recovery (`rocketnet-backups`)
Comprehensive backup management and disaster recovery.

**Key Tools:**
- `create_backup` - Create manual backups
- `restore_backup` - Restore from backups
- `schedule_backups` - Configure automatic backups

### 5. Analytics & Reporting (`rocketnet-analytics`)
Access CDN statistics, bandwidth usage, and visitor analytics.

**Key Tools:**
- `get_cdn_stats` - CDN usage statistics
- `visitor_analytics` - Traffic analysis
- `performance_metrics` - Site performance data

### 6. Billing & Account (`rocketnet-billing`)
Manage invoices, payments, and account settings.

**Key Tools:**
- `get_invoices` - Access billing history
- `update_payment` - Manage payment methods
- `change_plan` - Modify hosting plans

## Deployment

### Local Development

Each server can be run independently:

```bash
# Run sites management server
cd rocketnet-sites
fastmcp dev src/server.py

# Run WordPress management server
cd rocketnet-wordpress
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
├── rocketnet-shared/       # Shared utilities
├── rocketnet-sites/        # Sites management server
├── rocketnet-domains/      # Domains server
├── rocketnet-wordpress/    # WordPress server
├── rocketnet-backups/      # Backups server
├── rocketnet-analytics/    # Analytics server
├── rocketnet-billing/      # Billing server
├── README.md
├── SCRATCHPAD.md          # Development notes
└── DEPLOYMENT.md          # Deployment guide
```

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