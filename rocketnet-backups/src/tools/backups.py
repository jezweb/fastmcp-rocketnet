"""
Backup Management Tools for Rocket.net
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# Add parent directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import make_api_request
from utils import (
    format_success,
    format_error,
    format_warning,
    format_datetime,
    format_size,
)


async def create_backup(
    site_id: str,
    backup_type: str = "full",
    description: Optional[str] = None,
    notification_email: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a manual backup of a site.

    Args:
        site_id: The ID of the site to backup
        backup_type: Type of backup (full, database, files, incremental)
        description: Optional description for the backup
        notification_email: Email to notify when backup completes
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the created backup
    """
    try:
        payload = {
            "type": backup_type
        }

        if description:
            payload["description"] = description
        if notification_email:
            payload["notification_email"] = notification_email

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/backups",
            username=username,
            password=password,
            json_data=payload
        )
        backup = response.get("backup", response.get("data", response))

        return format_success(
            f"Backup initiated for site {site_id}",
            {
                "backup_id": backup.get("id"),
                "type": backup.get("type"),
                "status": backup.get("status", "in_progress"),
                "started_at": format_datetime(backup.get("started_at")),
                "estimated_completion": format_datetime(backup.get("estimated_completion")),
                "description": backup.get("description"),
                "message": "Backup is being created. This may take several minutes depending on site size."
            }
        )

    except Exception as e:
        return format_error(f"Failed to create backup for site {site_id}: {str(e)}")


async def list_backups(
    site_id: str,
    backup_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    List all backups for a site.

    Args:
        site_id: The ID of the site
        backup_type: Filter by backup type (full, database, files, incremental)
        status: Filter by status (completed, in_progress, failed)
        limit: Maximum number of backups to return

    Returns:
        List of backups with their details
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            params = {"limit": limit}
            if backup_type:
                params["type"] = backup_type
            if status:
                params["status"] = status

            response = await client.get(f"/sites/{site_id}/backups", params=params)
            backups = response.get("backups", response.get("data", []))

            formatted_backups = []
            for backup in backups:
                formatted_backups.append({
                    "id": backup.get("id"),
                    "type": backup.get("type"),
                    "status": backup.get("status"),
                    "size": format_size(backup.get("size", 0)),
                    "created_at": format_datetime(backup.get("created_at")),
                    "completed_at": format_datetime(backup.get("completed_at")),
                    "description": backup.get("description"),
                    "can_restore": backup.get("can_restore", True),
                    "expires_at": format_datetime(backup.get("expires_at"))
                })

            return format_success(
                f"Found {len(formatted_backups)} backups for site {site_id}",
                {
                    "backups": formatted_backups,
                    "count": len(formatted_backups),
                    "site_id": site_id
                }
            )

    except Exception as e:
        return format_error(f"Failed to list backups for site {site_id}: {str(e)}")


async def get_backup(
    site_id: str,
    backup_id: str
) -> Dict[str, Any]:
    """
    Get details of a specific backup.

    Args:
        site_id: The ID of the site
        backup_id: The ID of the backup

    Returns:
        Detailed backup information
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            response = await client.get(f"/sites/{site_id}/backups/{backup_id}")
            backup = response.get("backup", response.get("data", response))

            return format_success(
                f"Backup details retrieved",
                {
                    "id": backup.get("id"),
                    "site_id": site_id,
                    "type": backup.get("type"),
                    "status": backup.get("status"),
                    "size": format_size(backup.get("size", 0)),
                    "created_at": format_datetime(backup.get("created_at")),
                    "completed_at": format_datetime(backup.get("completed_at")),
                    "description": backup.get("description"),
                    "includes": {
                        "database": backup.get("includes_database", True),
                        "files": backup.get("includes_files", True),
                        "plugins": backup.get("includes_plugins", True),
                        "themes": backup.get("includes_themes", True),
                        "uploads": backup.get("includes_uploads", True),
                        "config": backup.get("includes_config", True)
                    },
                    "metadata": {
                        "wordpress_version": backup.get("wordpress_version"),
                        "php_version": backup.get("php_version"),
                        "mysql_version": backup.get("mysql_version")
                    },
                    "can_restore": backup.get("can_restore", True),
                    "expires_at": format_datetime(backup.get("expires_at")),
                    "download_available": backup.get("download_available", True)
                }
            )

    except Exception as e:
        return format_error(f"Failed to get backup {backup_id}: {str(e)}")


async def restore_backup(
    site_id: str,
    backup_id: str,
    restore_type: str = "full",
    confirm: bool = False
) -> Dict[str, Any]:
    """
    Restore a site from a backup. This will overwrite current site data!

    Args:
        site_id: The ID of the site to restore
        backup_id: The ID of the backup to restore from
        restore_type: Type of restore (full, database, files)
        confirm: Must be True to confirm restoration

    Returns:
        Information about the restoration process
    """
    try:
        if not confirm:
            return format_warning(
                "Restore requires confirmation",
                {
                    "message": "Set confirm=True to restore. This will overwrite current site data!",
                    "site_id": site_id,
                    "backup_id": backup_id,
                    "restore_type": restore_type
                }
            )

        config = Config.from_env()
        async with RocketnetClient(config) as client:
            payload = {
                "restore_type": restore_type
            }

            response = await client.post(
                f"/sites/{site_id}/backups/{backup_id}/restore",
                payload
            )
            restore = response.get("restore", response.get("data", response))

            return format_success(
                f"Restore initiated for site {site_id}",
                {
                    "restore_id": restore.get("id"),
                    "site_id": site_id,
                    "backup_id": backup_id,
                    "restore_type": restore_type,
                    "status": restore.get("status", "in_progress"),
                    "started_at": format_datetime(restore.get("started_at")),
                    "estimated_completion": format_datetime(restore.get("estimated_completion")),
                    "message": "Site is being restored. The site may be unavailable during this process."
                }
            )

    except Exception as e:
        return format_error(f"Failed to restore backup {backup_id}: {str(e)}")


async def download_backup(
    site_id: str,
    backup_id: str,
    expires_in: int = 3600
) -> Dict[str, Any]:
    """
    Get a temporary download link for a backup.

    Args:
        site_id: The ID of the site
        backup_id: The ID of the backup
        expires_in: Link expiration time in seconds (default: 1 hour)

    Returns:
        Download URL for the backup
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            payload = {"expires_in": expires_in}

            response = await client.post(
                f"/sites/{site_id}/backups/{backup_id}/download",
                payload
            )

            # Download info is in 'result' key
        download_info = response.get("result", response)

            return format_success(
                "Download link generated",
                {
                    "backup_id": backup_id,
                    "download_url": download_info.get("url"),
                    "expires_at": format_datetime(download_info.get("expires_at")),
                    "size": format_size(download_info.get("size", 0)),
                    "filename": download_info.get("filename"),
                    "checksum": download_info.get("checksum")
                }
            )

    except Exception as e:
        return format_error(f"Failed to get download link for backup {backup_id}: {str(e)}")


async def delete_backup(
    site_id: str,
    backup_id: str,
    confirm: bool = False
) -> Dict[str, Any]:
    """
    Delete a backup. This action is irreversible!

    Args:
        site_id: The ID of the site
        backup_id: The ID of the backup to delete
        confirm: Must be True to confirm deletion

    Returns:
        Confirmation of deletion
    """
    try:
        if not confirm:
            return format_warning(
                "Backup deletion requires confirmation",
                {"message": "Set confirm=True to delete the backup. This action cannot be undone!"}
            )

        config = Config.from_env()
        async with RocketnetClient(config) as client:
            await client.delete(f"/sites/{site_id}/backups/{backup_id}")

            return format_success(
                f"Backup {backup_id} deleted successfully",
                {
                    "site_id": site_id,
                    "deleted_backup_id": backup_id
                }
            )

    except Exception as e:
        return format_error(f"Failed to delete backup {backup_id}: {str(e)}")


async def test_restore(
    site_id: str,
    backup_id: str
) -> Dict[str, Any]:
    """
    Test restoration process without affecting the live site.
    Creates a staging environment with the backup restored.

    Args:
        site_id: The ID of the site
        backup_id: The ID of the backup to test

    Returns:
        Information about the test restoration
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            response = await client.post(
                f"/sites/{site_id}/backups/{backup_id}/test-restore"
            )
            test_restore = response.get("test_restore", response.get("data", response))

            return format_success(
                "Test restore initiated",
                {
                    "test_restore_id": test_restore.get("id"),
                    "staging_url": test_restore.get("staging_url"),
                    "status": test_restore.get("status", "in_progress"),
                    "expires_at": format_datetime(test_restore.get("expires_at")),
                    "message": "A staging environment is being created with the backup. You can test the restoration without affecting your live site."
                }
            )

    except Exception as e:
        return format_error(f"Failed to test restore backup {backup_id}: {str(e)}")


async def schedule_backup(
    site_id: str,
    frequency: str,
    backup_type: str = "full",
    retention_days: int = 30,
    time: Optional[str] = None
) -> Dict[str, Any]:
    """
    Set up automatic backup schedule for a site.

    Args:
        site_id: The ID of the site
        frequency: Backup frequency (daily, weekly, monthly)
        backup_type: Type of backup (full, database, files)
        retention_days: Number of days to retain backups
        time: Preferred backup time (HH:MM in UTC)

    Returns:
        Information about the backup schedule
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            payload = {
                "frequency": frequency,
                "backup_type": backup_type,
                "retention_days": retention_days
            }

            if time:
                payload["time"] = time

            response = await client.post(f"/sites/{site_id}/backup-schedule", payload)
            schedule = response.get("schedule", response.get("data", response))

            return format_success(
                f"Backup schedule created for site {site_id}",
                {
                    "schedule_id": schedule.get("id"),
                    "frequency": schedule.get("frequency"),
                    "backup_type": schedule.get("backup_type"),
                    "retention_days": schedule.get("retention_days"),
                    "next_backup": format_datetime(schedule.get("next_backup")),
                    "time": schedule.get("time"),
                    "enabled": schedule.get("enabled", True)
                }
            )

    except Exception as e:
        return format_error(f"Failed to schedule backup for site {site_id}: {str(e)}")


async def get_backup_schedule(site_id: str) -> Dict[str, Any]:
    """
    Get current backup schedule for a site.

    Args:
        site_id: The ID of the site

    Returns:
        Current backup schedule details
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            response = await client.get(f"/sites/{site_id}/backup-schedule")
            schedule = response.get("schedule", response.get("data", response))

            if not schedule:
                return format_warning(
                    "No backup schedule found",
                    {"site_id": site_id, "message": "This site does not have automatic backups configured"}
                )

            return format_success(
                "Backup schedule retrieved",
                {
                    "schedule_id": schedule.get("id"),
                    "frequency": schedule.get("frequency"),
                    "backup_type": schedule.get("backup_type"),
                    "retention_days": schedule.get("retention_days"),
                    "next_backup": format_datetime(schedule.get("next_backup")),
                    "last_backup": format_datetime(schedule.get("last_backup")),
                    "time": schedule.get("time"),
                    "enabled": schedule.get("enabled"),
                    "total_backups": schedule.get("total_backups", 0)
                }
            )

    except Exception as e:
        return format_error(f"Failed to get backup schedule for site {site_id}: {str(e)}")


async def update_backup_schedule(
    site_id: str,
    frequency: Optional[str] = None,
    backup_type: Optional[str] = None,
    retention_days: Optional[int] = None,
    time: Optional[str] = None,
    enabled: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Update backup schedule for a site.

    Args:
        site_id: The ID of the site
        frequency: New backup frequency
        backup_type: New backup type
        retention_days: New retention period
        time: New backup time
        enabled: Enable or disable the schedule

    Returns:
        Updated schedule information
    """
    try:
        config = Config.from_env()
        async with RocketnetClient(config) as client:
            payload = {}

            if frequency:
                payload["frequency"] = frequency
            if backup_type:
                payload["backup_type"] = backup_type
            if retention_days is not None:
                payload["retention_days"] = retention_days
            if time:
                payload["time"] = time
            if enabled is not None:
                payload["enabled"] = enabled

            if not payload:
                return format_warning("No updates provided")

            response = await client.patch(f"/sites/{site_id}/backup-schedule", payload)
            schedule = response.get("schedule", response.get("data", response))

            return format_success(
                "Backup schedule updated",
                {
                    "schedule_id": schedule.get("id"),
                    "frequency": schedule.get("frequency"),
                    "backup_type": schedule.get("backup_type"),
                    "retention_days": schedule.get("retention_days"),
                    "next_backup": format_datetime(schedule.get("next_backup")),
                    "time": schedule.get("time"),
                    "enabled": schedule.get("enabled")
                }
            )

    except Exception as e:
        return format_error(f"Failed to update backup schedule for site {site_id}: {str(e)}")


async def delete_backup_schedule(
    site_id: str,
    confirm: bool = False
) -> Dict[str, Any]:
    """
    Remove automatic backup schedule for a site.

    Args:
        site_id: The ID of the site
        confirm: Must be True to confirm deletion

    Returns:
        Confirmation of schedule deletion
    """
    try:
        if not confirm:
            return format_warning(
                "Schedule deletion requires confirmation",
                {"message": "Set confirm=True to delete the backup schedule. Automatic backups will stop!"}
            )

        config = Config.from_env()
        async with RocketnetClient(config) as client:
            await client.delete(f"/sites/{site_id}/backup-schedule")

            return format_success(
                "Backup schedule deleted",
                {
                    "site_id": site_id,
                    "message": "Automatic backups have been disabled for this site"
                }
            )

    except Exception as e:
        return format_error(f"Failed to delete backup schedule for site {site_id}: {str(e)}")


# Cloud Backup Functions
async def list_cloud_backups(
    site_id: str,
    limit: int = 50,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all cloud backups for a site.

    Args:
        site_id: The ID of the site
        limit: Maximum number of backups to return
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        List of cloud backups with details
    """
    try:
        params = {"limit": limit}

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/cloud-backups",
            params=params,
            username=username,
            password=password
        )
        backups = response.get("cloud_backups", response.get("data", []))

        formatted_backups = []
        for backup in backups:
            formatted_backups.append({
                "id": backup.get("id"),
                "name": backup.get("name"),
                "size": format_size(backup.get("size", 0)),
                "created_at": format_datetime(backup.get("created_at")),
                "provider": backup.get("provider", "Rocket.net Cloud"),
                "region": backup.get("region"),
                "encrypted": backup.get("encrypted", True),
                "status": backup.get("status")
            })

        return format_success(
            f"Found {len(formatted_backups)} cloud backups for site {site_id}",
            {
                "cloud_backups": formatted_backups,
                "count": len(formatted_backups),
                "site_id": site_id,
                "total_size": format_size(sum(b.get("size", 0) for b in backups))
            }
        )

    except Exception as e:
        return format_error(f"Failed to list cloud backups: {str(e)}")


async def create_cloud_backup(
    site_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    encrypt: bool = True,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new cloud backup for a site.

    Args:
        site_id: The ID of the site
        name: Optional name for the backup
        description: Optional description
        encrypt: Whether to encrypt the backup
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the created cloud backup
    """
    try:
        payload = {
            "encrypt": encrypt
        }
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/cloud-backups",
            json_data=payload,
            username=username,
            password=password
        )
        backup = response.get("cloud_backup", response.get("data", response))

        return format_success(
            f"Cloud backup initiated for site {site_id}",
            {
                "backup_id": backup.get("id"),
                "name": backup.get("name", name),
                "status": backup.get("status", "uploading"),
                "encrypted": encrypt,
                "provider": backup.get("provider", "Rocket.net Cloud"),
                "estimated_time": backup.get("estimated_time", "5-15 minutes"),
                "message": "Cloud backup is being created and uploaded"
            }
        )

    except Exception as e:
        return format_error(f"Failed to create cloud backup: {str(e)}")


async def get_cloud_backup(
    site_id: str,
    backup_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get details of a specific cloud backup.

    Args:
        site_id: The ID of the site
        backup_id: The ID of the cloud backup
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Detailed cloud backup information
    """
    try:
        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/cloud-backups/{backup_id}",
            username=username,
            password=password
        )
        backup = response.get("cloud_backup", response.get("data", response))

        return format_success(
            "Cloud backup details retrieved",
            {
                "id": backup.get("id"),
                "name": backup.get("name"),
                "site_id": site_id,
                "size": format_size(backup.get("size", 0)),
                "created_at": format_datetime(backup.get("created_at")),
                "status": backup.get("status"),
                "provider": backup.get("provider"),
                "region": backup.get("region"),
                "encrypted": backup.get("encrypted"),
                "checksum": backup.get("checksum"),
                "includes": backup.get("includes", {}),
                "download_available": backup.get("download_available", True),
                "restore_available": backup.get("restore_available", True)
            }
        )

    except Exception as e:
        return format_error(f"Failed to get cloud backup {backup_id}: {str(e)}")


async def delete_cloud_backup(
    site_id: str,
    backup_id: str,
    confirm: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a cloud backup. This action is irreversible!

    Args:
        site_id: The ID of the site
        backup_id: The ID of the cloud backup to delete
        confirm: Must be True to confirm deletion
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Confirmation of deletion
    """
    try:
        if not confirm:
            return format_warning(
                "Cloud backup deletion requires confirmation",
                {"message": "Set confirm=True to delete the cloud backup. This action cannot be undone!"}
            )

        await make_api_request(
            method="DELETE",
            endpoint=f"/sites/{site_id}/cloud-backups/{backup_id}",
            username=username,
            password=password
        )

        return format_success(
            f"Cloud backup {backup_id} deleted successfully",
            {
                "site_id": site_id,
                "deleted_backup_id": backup_id,
                "message": "Cloud backup has been permanently removed"
            }
        )

    except Exception as e:
        return format_error(f"Failed to delete cloud backup {backup_id}: {str(e)}")


async def download_cloud_backup(
    site_id: str,
    backup_id: str,
    expires_in: int = 3600,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a temporary download link for a cloud backup.

    Args:
        site_id: The ID of the site
        backup_id: The ID of the cloud backup
        expires_in: Link expiration time in seconds (default: 1 hour)
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Download URL for the cloud backup
    """
    try:
        params = {"expires_in": expires_in}

        response = await make_api_request(
            method="GET",
            endpoint=f"/sites/{site_id}/cloud-backups/{backup_id}/download",
            params=params,
            username=username,
            password=password
        )
        # Download info is in 'result' key
        download_info = response.get("result", response)

        return format_success(
            "Cloud backup download link generated",
            {
                "backup_id": backup_id,
                "download_url": download_info.get("url"),
                "expires_at": format_datetime(download_info.get("expires_at")),
                "size": format_size(download_info.get("size", 0)),
                "filename": download_info.get("filename"),
                "encrypted": download_info.get("encrypted", False)
            }
        )

    except Exception as e:
        return format_error(f"Failed to get download link for cloud backup {backup_id}: {str(e)}")


async def restore_cloud_backup(
    site_id: str,
    backup_id: str,
    target_site_id: Optional[str] = None,
    confirm: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Restore a site from a cloud backup or create a new site from backup.

    Args:
        site_id: The ID of the site that owns the backup
        backup_id: The ID of the cloud backup to restore
        target_site_id: Optional different site to restore to (creates new if not specified)
        confirm: Must be True to confirm restoration
        username: Rocket.net username (optional, uses env var if not provided)
        password: Rocket.net password (optional, uses env var if not provided)

    Returns:
        Information about the restoration process
    """
    try:
        if not confirm:
            return format_warning(
                "Cloud backup restore requires confirmation",
                {
                    "message": "Set confirm=True to restore. This will overwrite the target site!",
                    "source_site_id": site_id,
                    "backup_id": backup_id,
                    "target_site_id": target_site_id or site_id
                }
            )

        payload = {}
        if target_site_id:
            payload["target_site_id"] = target_site_id

        response = await make_api_request(
            method="POST",
            endpoint=f"/sites/{site_id}/cloud-backups/{backup_id}/restore",
            json_data=payload,
            username=username,
            password=password
        )
        restore = response.get("restore", response.get("data", response))

        return format_success(
            f"Cloud backup restore initiated",
            {
                "restore_id": restore.get("id"),
                "source_backup_id": backup_id,
                "target_site_id": target_site_id or site_id,
                "status": restore.get("status", "restoring"),
                "started_at": format_datetime(restore.get("started_at")),
                "estimated_completion": format_datetime(restore.get("estimated_completion")),
                "new_site_created": restore.get("new_site_created", False),
                "message": "Site is being restored from cloud backup"
            }
        )

    except Exception as e:
        return format_error(f"Failed to restore cloud backup {backup_id}: {str(e)}")