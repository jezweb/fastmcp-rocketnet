# Deployment Guide for Rocket.net MCP Servers

## Overview
This guide covers deployment options for the Rocket.net MCP servers, with a focus on FastMCP Cloud deployment for easy integration with Claude and other LLM applications.

## Table of Contents
1. [FastMCP Cloud Deployment](#fastmcp-cloud-deployment)
2. [Local Development](#local-development)
3. [Claude Desktop Integration](#claude-desktop-integration)
4. [Environment Configuration](#environment-configuration)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

## FastMCP Cloud Deployment

FastMCP Cloud provides the easiest way to deploy and use MCP servers with Claude.

### Prerequisites
- GitHub account
- FastMCP Cloud account (sign up at [fastmcp.cloud](https://fastmcp.cloud))
- Rocket.net API credentials

### Step-by-Step Deployment

#### 1. Fork or Use This Repository
- Fork this repository to your GitHub account, or
- Use this repository directly if you have access

#### 2. Connect to FastMCP Cloud
1. Go to [fastmcp.cloud](https://fastmcp.cloud)
2. Sign in with your GitHub account
3. Click "Deploy New Server"
4. Select your forked repository or search for `jezweb/fastmcp-rocketnet`

#### 3. Configure Servers
Each server can be deployed independently. Select which servers you need:

- **rocketnet-sites** - Core site management (recommended)
- **rocketnet-backups** - Backup operations
- **rocketnet-wordpress** - WordPress management
- **rocketnet-domains** - Domain management
- **rocketnet-analytics** - Reporting and analytics
- **rocketnet-billing** - Billing and account

#### 4. Set Environment Variables
For each server, configure the following environment variables in FastMCP Cloud:

```env
ROCKETNET_EMAIL=your-email@example.com
ROCKETNET_PASSWORD=your-password
```

Optional variables:
```env
ROCKETNET_API_BASE=https://control.rocket.net/api
ROCKETNET_RATE_LIMIT_REQUESTS=100
ROCKETNET_RATE_LIMIT_PERIOD=60
LOG_LEVEL=INFO
```

#### 5. Deploy
1. Click "Deploy" for each server
2. Wait for deployment to complete (usually < 1 minute)
3. Copy the server URL provided

#### 6. Add to Claude
1. Open Claude Desktop settings
2. Add the MCP server URL from FastMCP Cloud
3. The server will now be available in Claude conversations

## Local Development

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/jezweb/fastmcp-rocketnet.git
cd fastmcp-rocketnet
```

2. **Install shared package:**
```bash
cd rocketnet-shared
pip install -e .
cd ..
```

3. **Install server dependencies:**
```bash
cd rocketnet-sites  # or any other server
pip install -r requirements.txt
cd ..
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your Rocket.net credentials
```

### Running Servers Locally

#### Using FastMCP CLI:
```bash
# Run a single server
cd rocketnet-sites
fastmcp dev src/server.py

# The server will be available at http://localhost:5173
```

#### Using Python directly:
```bash
cd rocketnet-sites
python src/server.py
```

#### Running Multiple Servers:
Open multiple terminal windows and run each server on a different port:

```bash
# Terminal 1
cd rocketnet-sites
fastmcp dev src/server.py --port 5173

# Terminal 2
cd rocketnet-backups
fastmcp dev src/server.py --port 5174

# Terminal 3
cd rocketnet-wordpress
fastmcp dev src/server.py --port 5175
```

## Claude Desktop Integration

### Adding Local Servers

Edit your Claude Desktop configuration file:

**Mac/Linux:** `~/.claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\claude\claude_desktop_config.json`

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
    },
    "rocketnet-backups": {
      "command": "fastmcp",
      "args": ["dev", "/path/to/rocketnet-backups/src/server.py"],
      "env": {
        "ROCKETNET_EMAIL": "your-email@example.com",
        "ROCKETNET_PASSWORD": "your-password"
      }
    }
  }
}
```

### Using FastMCP Cloud URLs

After deploying to FastMCP Cloud, add the provided URLs:

```json
{
  "mcpServers": {
    "rocketnet": {
      "url": "https://your-server-id.fastmcp.cloud",
      "apiKey": "your-api-key-if-required"
    }
  }
}
```

## Environment Configuration

### Required Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ROCKETNET_EMAIL` | Your Rocket.net account email | Yes |
| `ROCKETNET_PASSWORD` | Your Rocket.net account password | Yes |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ROCKETNET_API_BASE` | API base URL | `https://control.rocket.net/api` |
| `ROCKETNET_RATE_LIMIT_REQUESTS` | Max requests per period | `100` |
| `ROCKETNET_RATE_LIMIT_PERIOD` | Rate limit period (seconds) | `60` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ROCKETNET_TIMEOUT` | Request timeout (seconds) | `30` |
| `ROCKETNET_MAX_RETRIES` | Max retry attempts | `3` |
| `ROCKETNET_RETRY_DELAY` | Initial retry delay (seconds) | `1` |

### Security Best Practices

1. **Never commit credentials** to the repository
2. **Use environment variables** for all sensitive data
3. **Rotate passwords regularly**
4. **Use strong, unique passwords**
5. **Enable 2FA** on your Rocket.net account
6. **Limit API access** to specific IP addresses if possible

## Testing

### Unit Tests

Run tests for individual servers:

```bash
cd rocketnet-sites
pytest tests/
```

### Integration Tests

Test with actual API (requires valid credentials):

```bash
export ROCKETNET_EMAIL=your-email@example.com
export ROCKETNET_PASSWORD=your-password
pytest tests/integration/
```

### Manual Testing

Use the FastMCP test interface:

```bash
fastmcp dev src/server.py
# Open http://localhost:5173 in your browser
```

## Troubleshooting

### Common Issues

#### "Authentication failed"
- Verify your email and password are correct
- Check if your account has API access enabled
- Ensure environment variables are set correctly

#### "Rate limit exceeded"
- The servers implement automatic retry with backoff
- Adjust `ROCKETNET_RATE_LIMIT_REQUESTS` if needed
- Consider using fewer parallel requests

#### "Module not found" errors
- Ensure the shared package is installed: `pip install -e rocketnet-shared`
- Check Python path includes the parent directory
- Verify all dependencies are installed

#### "Connection timeout"
- Check your internet connection
- Verify Rocket.net API is accessible
- Increase `ROCKETNET_TIMEOUT` if needed

### Debug Mode

Enable debug logging for more information:

```bash
export LOG_LEVEL=DEBUG
fastmcp dev src/server.py
```

### Getting Help

1. Check the [GitHub Issues](https://github.com/jezweb/fastmcp-rocketnet/issues)
2. Consult the [Rocket.net API documentation](https://rocketdotnet.readme.io)
3. Visit [FastMCP documentation](https://github.com/jlowin/fastmcp)
4. Contact support at jeremy@jezweb.net

## Production Considerations

### Performance Optimization

1. **Deploy only needed servers** - Don't deploy all servers if you only need site management
2. **Use caching** - The client implements response caching where appropriate
3. **Batch operations** - Use bulk endpoints when available
4. **Monitor rate limits** - Adjust rate limiting based on your usage patterns

### Monitoring

1. **Use FastMCP Cloud monitoring** - Built-in monitoring and logging
2. **Set up alerts** - Configure alerts for errors or high latency
3. **Track usage** - Monitor API usage to stay within limits

### Scaling

1. **Horizontal scaling** - Deploy multiple instances of high-use servers
2. **Load balancing** - Use FastMCP Cloud's built-in load balancing
3. **Regional deployment** - Deploy closer to your users for lower latency

## Updates and Maintenance

### Updating Servers

1. **Pull latest changes:**
```bash
git pull origin main
```

2. **Update dependencies:**
```bash
cd rocketnet-shared
pip install -U -e .
cd ../rocketnet-sites
pip install -U -r requirements.txt
```

3. **Redeploy to FastMCP Cloud:**
- Push changes to GitHub
- FastMCP Cloud will automatically redeploy

### Version Management

- Check `CHANGELOG.md` for version history
- Use semantic versioning for releases
- Test thoroughly before deploying updates

## Support

For issues, questions, or contributions:
- GitHub: [github.com/jezweb/fastmcp-rocketnet](https://github.com/jezweb/fastmcp-rocketnet)
- Email: jeremy@jezweb.net
- Website: [www.jezweb.com.au](https://www.jezweb.com.au)