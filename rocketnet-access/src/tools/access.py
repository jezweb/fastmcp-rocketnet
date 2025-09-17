"""
Site Access Management Tools for Rocket.net
Handles SSH keys, FTP accounts, file management, staging, and access control
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add parent directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import make_api_request
from utils import format_success, format_error, format_warning, format_datetime


# SSH Key Management
async def list_ssh_keys(
    site_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all SSH keys for a site.

    Args:
        site_id: The ID of the site
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of SSH keys configured for the site
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/ssh-keys",
            username=username,
            password=password
        )
        keys = response.get("ssh_keys", response.get("data", []))

        formatted_keys = []
        for key in keys:
            formatted_keys.append({
                "name": key.get("name"),
                "fingerprint": key.get("fingerprint"),
                "type": key.get("type"),
                "authorized": key.get("authorized", False),
                "added_at": format_datetime(key.get("added_at"))
            })

        return format_success(
            f"Found {len(formatted_keys)} SSH keys for site {site_id}",
            {
                "ssh_keys": formatted_keys,
                "count": len(formatted_keys),
                "authorized_count": sum(1 for k in formatted_keys if k["authorized"])
            }
        )

    except Exception as e:
        return format_error(f"Failed to list SSH keys: {str(e)}")


async def add_ssh_key(
    site_id: str,
    name: str,
    public_key: str,
    authorize: bool = True,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add an SSH key to a site.

    Args:
        site_id: The ID of the site
        name: Name for the SSH key
        public_key: The public SSH key content
        authorize: Whether to immediately authorize the key
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the added SSH key
    """
    try:
        payload = {
            "name": name,
            "public_key": public_key,
            "authorize": authorize
        }

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/ssh-keys",
            json_data=payload,
            username=username,
            password=password
        )
        key_info = response.get("ssh_key", response.get("data", response))

        return format_success(
            f"SSH key '{name}' added to site {site_id}",
            {
                "name": name,
                "fingerprint": key_info.get("fingerprint"),
                "authorized": authorize,
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to add SSH key: {str(e)}")


async def authorize_ssh_key(
    site_id: str,
    key_name: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Authorize an SSH key for site access.

    Args:
        site_id: The ID of the site
        key_name: Name of the SSH key to authorize
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of authorization
    """
    try:
        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/ssh-keys/authorize",
            json_data={"name": key_name},
            username=username,
            password=password
        )

        return format_success(
            f"SSH key '{key_name}' authorized",
            {
                "key_name": key_name,
                "site_id": site_id,
                "status": "authorized"
            }
        )

    except Exception as e:
        return format_error(f"Failed to authorize SSH key: {str(e)}")


async def delete_ssh_key(
    site_id: str,
    key_name: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove an SSH key from a site.

    Args:
        site_id: The ID of the site
        key_name: Name of the SSH key to remove
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of removal
    """
    try:
        await make_api_request(
            method="DELETE",
            endpoint=f"/sites/{site_id}/ssh-keys",
            params={"name": key_name},
            username=username,
            password=password
        )

        return format_success(
            f"SSH key '{key_name}' removed",
            {
                "removed_key": key_name,
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to delete SSH key: {str(e)}")


# FTP Account Management
async def list_ftp_accounts(
    site_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all FTP accounts for a site.

    Args:
        site_id: The ID of the site
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of FTP accounts
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/ftp-accounts",
            username=username,
            password=password
        )
        accounts = response.get("ftp_accounts", response.get("data", []))

        formatted_accounts = []
        for account in accounts:
            formatted_accounts.append({
                "username": account.get("username"),
                "path": account.get("path", "/"),
                "created_at": format_datetime(account.get("created_at")),
                "last_login": format_datetime(account.get("last_login")),
                "status": account.get("status", "active")
            })

        return format_success(
            f"Found {len(formatted_accounts)} FTP accounts",
            {
                "ftp_accounts": formatted_accounts,
                "count": len(formatted_accounts),
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to list FTP accounts: {str(e)}")


async def create_ftp_account(
    site_id: str,
    username: str,
    password: str,
    path: str = "/",
    ftp_username: Optional[str] = None,
    ftp_password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new FTP account for a site.

    Args:
        site_id: The ID of the site
        username: FTP username to create
        password: FTP password
        path: Directory path for FTP access (default: root)
        ftp_username: Rocket.net username (optional, uses env var if not provided)
        ftp_password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the created FTP account
    """
    try:
        payload = {
            "username": username,
            "password": password,
            "path": path
        }

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/ftp-accounts",
            json_data=payload,
            username=ftp_username,
            password=ftp_password
        )
        account = response.get("ftp_account", response.get("data", response))

        return format_success(
            f"FTP account '{username}' created",
            {
                "username": username,
                "path": path,
                "site_id": site_id,
                "host": account.get("host"),
                "port": account.get("port", 21)
            }
        )

    except Exception as e:
        return format_error(f"Failed to create FTP account: {str(e)}")


async def delete_ftp_account(
    site_id: str,
    username: str,
    rocket_username: Optional[str] = None,
    rocket_password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete an FTP account from a site.

    Args:
        site_id: The ID of the site
        username: FTP username to delete
        rocket_username: Rocket.net username (optional, uses env var if not provided)
        rocket_password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of deletion
    """
    try:
        await make_api_request(
            method="DELETE",
            endpoint=f"/sites/{site_id}/ftp-accounts",
            params={"username": username},
            username=rocket_username,
            password=rocket_password
        )

        return format_success(
            f"FTP account '{username}' deleted",
            {
                "deleted_account": username,
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to delete FTP account: {str(e)}")


# File Management
async def list_files(
    site_id: str,
    path: str = "/",
    show_hidden: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List files in a site directory.

    Args:
        site_id: The ID of the site
        path: Directory path to list (default: root)
        show_hidden: Whether to show hidden files
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of files and directories
    """
    try:
        params = {
            "path": path,
            "show_hidden": show_hidden
        }

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/file-manager/files",
            params=params,
            username=username,
            password=password
        )
        files = response.get("files", response.get("data", []))

        formatted_files = []
        for file in files:
            formatted_files.append({
                "name": file.get("name"),
                "type": file.get("type"),
                "size": file.get("size"),
                "modified": format_datetime(file.get("modified")),
                "permissions": file.get("permissions"),
                "path": file.get("path")
            })

        return format_success(
            f"Found {len(formatted_files)} items in {path}",
            {
                "path": path,
                "files": formatted_files,
                "count": len(formatted_files),
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to list files: {str(e)}")


async def upload_file(
    site_id: str,
    local_file_path: str,
    remote_path: str,
    overwrite: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Upload a file to the site.

    Args:
        site_id: The ID of the site
        local_file_path: Path to local file to upload
        remote_path: Remote destination path
        overwrite: Whether to overwrite existing file
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the uploaded file
    """
    try:
        # Read the local file
        with open(local_file_path, 'rb') as f:
            file_content = f.read()

        payload = {
            "path": remote_path,
            "content": file_content.decode('utf-8') if isinstance(file_content, bytes) else file_content,
            "overwrite": overwrite
        }

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/files",
            json_data=payload,
            username=username,
            password=password
        )
        file_info = response.get("file", response.get("data", response))

        return format_success(
            f"File uploaded to {remote_path}",
            {
                "remote_path": remote_path,
                "size": file_info.get("size"),
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to upload file: {str(e)}")


async def delete_file(
    site_id: str,
    file_path: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a file from the site.

    Args:
        site_id: The ID of the site
        file_path: Path to the file to delete
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of deletion
    """
    try:
        await make_api_request(
            method="DELETE",
            endpoint=f"/sites/{site_id}/files",
            params={"path": file_path},
            username=username,
            password=password
        )

        return format_success(
            f"File deleted: {file_path}",
            {
                "deleted_file": file_path,
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to delete file: {str(e)}")


async def compress_files(
    site_id: str,
    paths: List[str],
    archive_name: str,
    archive_type: str = "zip",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Compress files or folders into an archive.

    Args:
        site_id: The ID of the site
        paths: List of file/folder paths to compress
        archive_name: Name for the archive
        archive_type: Type of archive (zip, tar, tar.gz)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the created archive
    """
    try:
        payload = {
            "paths": paths,
            "archive_name": archive_name,
            "type": archive_type
        }

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/files/compress",
            json_data=payload,
            username=username,
            password=password
        )
        archive = response.get("archive", response.get("data", response))

        return format_success(
            f"Archive created: {archive_name}",
            {
                "archive_name": archive_name,
                "archive_type": archive_type,
                "size": archive.get("size"),
                "path": archive.get("path"),
                "files_count": len(paths)
            }
        )

    except Exception as e:
        return format_error(f"Failed to compress files: {str(e)}")


async def extract_archive(
    site_id: str,
    archive_path: str,
    destination: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extract an archive file.

    Args:
        site_id: The ID of the site
        archive_path: Path to the archive to extract
        destination: Destination directory (optional, uses archive location)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the extraction
    """
    try:
        payload = {
            "archive_path": archive_path
        }
        if destination:
            payload["destination"] = destination

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/files/extract",
            json_data=payload,
            username=username,
            password=password
        )
        result = response.get("result", response.get("data", response))

        return format_success(
            f"Archive extracted: {archive_path}",
            {
                "archive_path": archive_path,
                "destination": destination or "Same directory",
                "files_extracted": result.get("files_count"),
                "site_id": site_id
            }
        )

    except Exception as e:
        return format_error(f"Failed to extract archive: {str(e)}")


# Staging Sites
async def create_staging_site(
    site_id: str,
    staging_name: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a staging environment for a site.

    Args:
        site_id: The ID of the site
        staging_name: Optional name for the staging site
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the staging site
    """
    try:
        payload = {}
        if staging_name:
            payload["name"] = staging_name

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/staging",
            json_data=payload,
            username=username,
            password=password
        )
        staging = response.get("staging", response.get("data", response))

        return format_success(
            f"Staging site created for site {site_id}",
            {
                "staging_id": staging.get("id"),
                "staging_url": staging.get("url"),
                "status": staging.get("status", "creating"),
                "parent_site_id": site_id,
                "message": "Staging site is being created. This may take a few minutes."
            }
        )

    except Exception as e:
        return format_error(f"Failed to create staging site: {str(e)}")


async def publish_staging(
    site_id: str,
    backup_production: bool = True,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Publish staging site to production.

    Args:
        site_id: The ID of the site with staging
        backup_production: Whether to backup production before publishing
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the publish operation
    """
    try:
        payload = {
            "backup_production": backup_production
        }

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/staging/publish",
            json_data=payload,
            username=username,
            password=password
        )
        result = response.get("result", response.get("data", response))

        return format_success(
            "Staging site publishing to production",
            {
                "site_id": site_id,
                "backup_created": backup_production,
                "status": result.get("status", "publishing"),
                "estimated_time": result.get("estimated_time", "5-10 minutes"),
                "message": "Production site will be replaced with staging content"
            }
        )

    except Exception as e:
        return format_error(f"Failed to publish staging: {str(e)}")


async def delete_staging_site(
    site_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete the staging environment for a site.

    Args:
        site_id: The ID of the site
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of deletion
    """
    try:
        await make_api_request(
            method="DELETE",
            endpoint=f"/sites/{site_id}/staging",
            username=username,
            password=password
        )

        return format_success(
            "Staging site deleted",
            {
                "site_id": site_id,
                "message": "Staging environment has been removed"
            }
        )

    except Exception as e:
        return format_error(f"Failed to delete staging site: {str(e)}")


# phpMyAdmin Access
async def get_phpmyadmin_login(
    site_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get SSO login URL for phpMyAdmin.

    Args:
        site_id: The ID of the site
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        phpMyAdmin SSO login URL
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/pma_login",
            username=username,
            password=password
        )
        login_info = response.get("login", response.get("data", response))

        return format_success(
            "phpMyAdmin SSO URL generated",
            {
                "site_id": site_id,
                "login_url": login_info.get("url"),
                "expires_at": format_datetime(login_info.get("expires_at")),
                "message": "This is a one-time login URL for phpMyAdmin access"
            }
        )

    except Exception as e:
        return format_error(f"Failed to get phpMyAdmin login: {str(e)}")


# Password Protection
async def get_password_protection_status(
    site_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get password protection status for a site.

    Args:
        site_id: The ID of the site
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Password protection status and settings
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/password-protection",
            username=username,
            password=password
        )
        protection = response.get("protection", response.get("data", response))

        return format_success(
            "Password protection status retrieved",
            {
                "site_id": site_id,
                "enabled": protection.get("enabled", False),
                "message": protection.get("message", "Please enter password to access site"),
                "users_count": protection.get("users_count", 0),
                "exclude_paths": protection.get("exclude_paths", [])
            }
        )

    except Exception as e:
        return format_error(f"Failed to get password protection status: {str(e)}")


async def enable_password_protection(
    site_id: str,
    message: str = "This site is password protected",
    exclude_paths: Optional[List[str]] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Enable password protection for a site.

    Args:
        site_id: The ID of the site
        message: Message to display on password prompt
        exclude_paths: Paths to exclude from protection
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of password protection enablement
    """
    try:
        payload = {
            "message": message
        }
        if exclude_paths:
            payload["exclude_paths"] = exclude_paths

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/password-protection",
            json_data=payload,
            username=username,
            password=password
        )

        return format_success(
            "Password protection enabled",
            {
                "site_id": site_id,
                "enabled": True,
                "message": message,
                "exclude_paths": exclude_paths or [],
                "note": "Add users to grant access"
            }
        )

    except Exception as e:
        return format_error(f"Failed to enable password protection: {str(e)}")


async def add_password_user(
    site_id: str,
    user: str,
    password: str,
    rocket_username: Optional[str] = None,
    rocket_password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a user for password-protected site access.

    Args:
        site_id: The ID of the site
        user: Username for site access
        password: Password for site access
        rocket_username: Rocket.net username (optional, uses env var if not provided)
        rocket_password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the added user
    """
    try:
        payload = {
            "username": user,
            "password": password
        }

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/password-protection/users",
            json_data=payload,
            username=rocket_username,
            password=rocket_password
        )

        return format_success(
            f"Password protection user '{user}' added",
            {
                "site_id": site_id,
                "username": user,
                "message": "User can now access the password-protected site"
            }
        )

    except Exception as e:
        return format_error(f"Failed to add password user: {str(e)}")