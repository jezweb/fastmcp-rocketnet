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

            download_info = response.get("download", response.get("data", response))

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