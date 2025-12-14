"""
Instagram Downloader - Core Package
"""

__version__ = "1.0.0"
__author__ = "Instagram Downloader Team"

from .main import (
    InstagramDownloaderConfig,
    SessionManager,
    InstagramProfileDownloader
)

from .advanced import (
    RateLimiter,
    ExponentialBackoffRetry,
    InstagramAPIWrapper
)

__all__ = [
    'InstagramDownloaderConfig',
    'SessionManager',
    'InstagramProfileDownloader',
    'RateLimiter',
    'ExponentialBackoffRetry',
    'InstagramAPIWrapper',
]
