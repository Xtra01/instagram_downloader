#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Storage Cleanup Manager for Web Deployment
Prevents disk overflow by auto-cleaning old downloads
"""

import os
import shutil
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
import threading

logger = logging.getLogger(__name__)


class StorageCleanupManager:
    """Manages automatic cleanup of downloaded files"""
    
    def __init__(
        self, 
        download_folder: Path,
        max_age_hours: int = 24,  # Files older than 24 hours will be deleted
        max_storage_mb: int = 5000,  # Max 5 GB storage
        cleanup_interval_seconds: int = 3600  # Check every hour
    ):
        self.download_folder = Path(download_folder)
        self.max_age_hours = max_age_hours
        self.max_storage_mb = max_storage_mb
        self.max_storage_bytes = max_storage_mb * 1024 * 1024
        self.cleanup_interval = cleanup_interval_seconds
        self.is_running = False
        self._cleanup_thread: Optional[threading.Thread] = None
        
    def get_folder_size(self, folder: Path) -> int:
        """Calculate total size of a folder in bytes"""
        total_size = 0
        try:
            for entry in folder.rglob('*'):
                if entry.is_file():
                    total_size += entry.stat().st_size
        except Exception as e:
            logger.error(f"Error calculating folder size: {e}")
        return total_size
    
    def get_old_files(self, max_age_hours: int) -> list:
        """Get files older than specified hours"""
        now = datetime.now()
        cutoff_time = now - timedelta(hours=max_age_hours)
        old_files = []
        
        try:
            for entry in self.download_folder.rglob('*'):
                if entry.is_file():
                    file_time = datetime.fromtimestamp(entry.stat().st_mtime)
                    if file_time < cutoff_time:
                        old_files.append({
                            'path': entry,
                            'size': entry.stat().st_size,
                            'age_hours': (now - file_time).total_seconds() / 3600
                        })
        except Exception as e:
            logger.error(f"Error finding old files: {e}")
        
        return old_files
    
    def cleanup_by_age(self) -> dict:
        """Delete files older than max_age_hours"""
        deleted_count = 0
        freed_bytes = 0
        errors = []
        
        old_files = self.get_old_files(self.max_age_hours)
        
        for file_info in old_files:
            try:
                file_path = file_info['path']
                file_size = file_info['size']
                file_path.unlink()
                deleted_count += 1
                freed_bytes += file_size
                logger.info(f"Deleted old file: {file_path.name} ({file_info['age_hours']:.1f} hours old)")
            except Exception as e:
                errors.append(str(e))
                logger.error(f"Error deleting {file_path}: {e}")
        
        # Clean up empty directories
        self._cleanup_empty_dirs()
        
        return {
            'deleted_count': deleted_count,
            'freed_mb': freed_bytes / (1024 * 1024),
            'errors': errors
        }
    
    def cleanup_by_size(self) -> dict:
        """Delete oldest files if storage exceeds limit"""
        current_size = self.get_folder_size(self.download_folder)
        
        if current_size <= self.max_storage_bytes:
            return {
                'deleted_count': 0,
                'freed_mb': 0,
                'current_size_mb': current_size / (1024 * 1024),
                'max_size_mb': self.max_storage_mb
            }
        
        # Get all files sorted by modification time (oldest first)
        files = []
        try:
            for entry in self.download_folder.rglob('*'):
                if entry.is_file():
                    files.append({
                        'path': entry,
                        'size': entry.stat().st_size,
                        'mtime': entry.stat().st_mtime
                    })
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return {'error': str(e)}
        
        files.sort(key=lambda x: x['mtime'])
        
        # Delete oldest files until we're under the limit
        deleted_count = 0
        freed_bytes = 0
        
        for file_info in files:
            if current_size - freed_bytes <= self.max_storage_bytes:
                break
            
            try:
                file_path = file_info['path']
                file_size = file_info['size']
                file_path.unlink()
                deleted_count += 1
                freed_bytes += file_size
                logger.info(f"Deleted file to free space: {file_path.name}")
            except Exception as e:
                logger.error(f"Error deleting {file_path}: {e}")
        
        # Clean up empty directories
        self._cleanup_empty_dirs()
        
        return {
            'deleted_count': deleted_count,
            'freed_mb': freed_bytes / (1024 * 1024),
            'current_size_mb': (current_size - freed_bytes) / (1024 * 1024),
            'max_size_mb': self.max_storage_mb
        }
    
    def _cleanup_empty_dirs(self):
        """Remove empty directories (DISABLED - prevents interference with active downloads)"""
        # Disabled to prevent accidental deletion of folders during download process
        pass
    
    def perform_cleanup(self) -> dict:
        """Perform full cleanup (age and size based)"""
        logger.info("Starting storage cleanup...")
        
        # First cleanup old files
        age_result = self.cleanup_by_age()
        
        # Then cleanup by size if needed
        size_result = self.cleanup_by_size()
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'age_cleanup': age_result,
            'size_cleanup': size_result,
            'current_storage_mb': self.get_folder_size(self.download_folder) / (1024 * 1024)
        }
        
        logger.info(f"Cleanup complete: {result}")
        return result
    
    def _cleanup_loop(self):
        """Background cleanup loop"""
        logger.info("Storage cleanup background thread started")
        
        while self.is_running:
            try:
                self.perform_cleanup()
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
            
            # Wait for next cleanup cycle
            time.sleep(self.cleanup_interval)
        
        logger.info("Storage cleanup background thread stopped")
    
    def start_background_cleanup(self):
        """Start automatic cleanup in background thread"""
        if self.is_running:
            logger.warning("Cleanup thread already running")
            return
        
        self.is_running = True
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_loop,
            daemon=True,
            name="StorageCleanup"
        )
        self._cleanup_thread.start()
        logger.info(f"Started background cleanup (interval: {self.cleanup_interval}s, max_age: {self.max_age_hours}h, max_size: {self.max_storage_mb}MB)")
    
    def stop_background_cleanup(self):
        """Stop background cleanup"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self._cleanup_thread:
            self._cleanup_thread.join(timeout=5)
        logger.info("Stopped background cleanup")
    
    def get_storage_stats(self) -> dict:
        """Get current storage statistics"""
        total_size = self.get_folder_size(self.download_folder)
        
        file_count = 0
        oldest_file_time = None
        newest_file_time = None
        
        try:
            for entry in self.download_folder.rglob('*'):
                if entry.is_file():
                    file_count += 1
                    mtime = datetime.fromtimestamp(entry.stat().st_mtime)
                    if oldest_file_time is None or mtime < oldest_file_time:
                        oldest_file_time = mtime
                    if newest_file_time is None or mtime > newest_file_time:
                        newest_file_time = mtime
        except Exception as e:
            logger.error(f"Error getting storage stats: {e}")
        
        return {
            'total_size_mb': total_size / (1024 * 1024),
            'total_size_gb': total_size / (1024 * 1024 * 1024),
            'max_size_mb': self.max_storage_mb,
            'usage_percent': (total_size / self.max_storage_bytes) * 100 if self.max_storage_bytes > 0 else 0,
            'file_count': file_count,
            'oldest_file': oldest_file_time.isoformat() if oldest_file_time else None,
            'newest_file': newest_file_time.isoformat() if newest_file_time else None
        }


# Usage example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    cleanup_manager = StorageCleanupManager(
        download_folder=Path("downloads"),
        max_age_hours=24,
        max_storage_mb=5000,
        cleanup_interval_seconds=3600
    )
    
    # Get stats
    stats = cleanup_manager.get_storage_stats()
    print(f"Storage Stats: {stats}")
    
    # Perform cleanup
    result = cleanup_manager.perform_cleanup()
    print(f"Cleanup Result: {result}")
