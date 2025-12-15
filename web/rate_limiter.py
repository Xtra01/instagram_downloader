#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rate Limiting Manager for Web Deployment
Prevents abuse and protects from bans
"""

import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Optional
import threading

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiting for API endpoints"""
    
    def __init__(
        self,
        max_requests_per_minute: int = 10,
        max_requests_per_hour: int = 100,
        max_downloads_per_day: int = 500,
        cooldown_after_ban: int = 3600  # 1 hour cooldown
    ):
        self.max_per_minute = max_requests_per_minute
        self.max_per_hour = max_requests_per_hour
        self.max_per_day = max_downloads_per_day
        self.cooldown_seconds = cooldown_after_ban
        
        # Track requests per IP
        self._requests: Dict[str, list] = defaultdict(list)
        self._downloads: Dict[str, list] = defaultdict(list)
        self._banned_ips: Dict[str, float] = {}
        
        # Lock for thread safety
        self._lock = threading.Lock()
        
        # Cleanup thread
        self._cleanup_thread: Optional[threading.Thread] = None
        self._is_running = False
    
    def _cleanup_old_entries(self):
        """Remove old entries to prevent memory growth"""
        now = time.time()
        cutoff_minute = now - 60
        cutoff_hour = now - 3600
        cutoff_day = now - 86400
        
        with self._lock:
            # Cleanup requests
            for ip in list(self._requests.keys()):
                self._requests[ip] = [ts for ts in self._requests[ip] if ts > cutoff_hour]
                if not self._requests[ip]:
                    del self._requests[ip]
            
            # Cleanup downloads
            for ip in list(self._downloads.keys()):
                self._downloads[ip] = [ts for ts in self._downloads[ip] if ts > cutoff_day]
                if not self._downloads[ip]:
                    del self._downloads[ip]
            
            # Cleanup bans
            for ip in list(self._banned_ips.keys()):
                if now - self._banned_ips[ip] > self.cooldown_seconds:
                    del self._banned_ips[ip]
                    logger.info(f"IP unbanned: {ip}")
    
    def _cleanup_loop(self):
        """Background cleanup"""
        while self._is_running:
            try:
                self._cleanup_old_entries()
            except Exception as e:
                logger.error(f"Cleanup error: {e}")
            time.sleep(300)  # Every 5 minutes
    
    def start_background_cleanup(self):
        """Start cleanup thread"""
        if self._is_running:
            return
        
        self._is_running = True
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_loop,
            daemon=True,
            name="RateLimitCleanup"
        )
        self._cleanup_thread.start()
        logger.info("Started rate limit cleanup thread")
    
    def stop_background_cleanup(self):
        """Stop cleanup thread"""
        self._is_running = False
        if self._cleanup_thread:
            self._cleanup_thread.join(timeout=5)
    
    def is_banned(self, ip: str) -> bool:
        """Check if IP is banned"""
        with self._lock:
            if ip in self._banned_ips:
                ban_time = self._banned_ips[ip]
                if time.time() - ban_time < self.cooldown_seconds:
                    return True
                else:
                    del self._banned_ips[ip]
            return False
    
    def ban_ip(self, ip: str, reason: str = "Rate limit exceeded"):
        """Ban an IP temporarily"""
        with self._lock:
            self._banned_ips[ip] = time.time()
            logger.warning(f"IP banned: {ip} - Reason: {reason}")
    
    def check_rate_limit(self, ip: str, is_download: bool = False) -> dict:
        """
        Check if request is allowed
        
        Returns:
            dict: {'allowed': bool, 'reason': str, 'retry_after': int}
        """
        now = time.time()
        
        # Check if banned
        if self.is_banned(ip):
            remaining_cooldown = int(self.cooldown_seconds - (now - self._banned_ips.get(ip, now)))
            return {
                'allowed': False,
                'reason': 'IP temporarily banned due to excessive requests',
                'retry_after': remaining_cooldown
            }
        
        with self._lock:
            # Add current request
            self._requests[ip].append(now)
            if is_download:
                self._downloads[ip].append(now)
            
            # Check minute limit
            last_minute = [ts for ts in self._requests[ip] if now - ts < 60]
            if len(last_minute) > self.max_per_minute:
                self.ban_ip(ip, f"Exceeded {self.max_per_minute} requests per minute")
                return {
                    'allowed': False,
                    'reason': f'Rate limit: Maximum {self.max_per_minute} requests per minute',
                    'retry_after': 60
                }
            
            # Check hour limit
            last_hour = [ts for ts in self._requests[ip] if now - ts < 3600]
            if len(last_hour) > self.max_per_hour:
                self.ban_ip(ip, f"Exceeded {self.max_per_hour} requests per hour")
                return {
                    'allowed': False,
                    'reason': f'Rate limit: Maximum {self.max_per_hour} requests per hour',
                    'retry_after': 3600
                }
            
            # Check daily download limit
            if is_download:
                last_day = [ts for ts in self._downloads[ip] if now - ts < 86400]
                if len(last_day) > self.max_per_day:
                    self.ban_ip(ip, f"Exceeded {self.max_per_day} downloads per day")
                    return {
                        'allowed': False,
                        'reason': f'Rate limit: Maximum {self.max_per_day} downloads per day',
                        'retry_after': 86400
                    }
        
        return {
            'allowed': True,
            'reason': 'OK',
            'retry_after': 0
        }
    
    def get_stats(self, ip: str) -> dict:
        """Get usage stats for an IP"""
        now = time.time()
        
        with self._lock:
            requests_last_minute = len([ts for ts in self._requests.get(ip, []) if now - ts < 60])
            requests_last_hour = len([ts for ts in self._requests.get(ip, []) if now - ts < 3600])
            downloads_last_day = len([ts for ts in self._downloads.get(ip, []) if now - ts < 86400])
            
            is_banned = ip in self._banned_ips
            ban_remaining = 0
            if is_banned:
                ban_remaining = int(self.cooldown_seconds - (now - self._banned_ips[ip]))
            
            return {
                'ip': ip,
                'requests_last_minute': requests_last_minute,
                'requests_last_hour': requests_last_hour,
                'downloads_last_day': downloads_last_day,
                'is_banned': is_banned,
                'ban_remaining_seconds': ban_remaining,
                'limits': {
                    'per_minute': self.max_per_minute,
                    'per_hour': self.max_per_hour,
                    'per_day': self.max_per_day
                }
            }
    
    def get_all_stats(self) -> dict:
        """Get global statistics"""
        with self._lock:
            total_ips = len(self._requests)
            total_banned = len(self._banned_ips)
            
            total_requests_last_minute = sum(
                len([ts for ts in requests if time.time() - ts < 60])
                for requests in self._requests.values()
            )
            
            total_requests_last_hour = sum(
                len([ts for ts in requests if time.time() - ts < 3600])
                for requests in self._requests.values()
            )
            
            total_downloads_last_day = sum(
                len([ts for ts in downloads if time.time() - ts < 86400])
                for downloads in self._downloads.values()
            )
            
            return {
                'total_active_ips': total_ips,
                'total_banned_ips': total_banned,
                'requests_last_minute': total_requests_last_minute,
                'requests_last_hour': total_requests_last_hour,
                'downloads_last_day': total_downloads_last_day
            }


# Flask decorator for easy use
def rate_limit_decorator(limiter: RateLimiter, is_download: bool = False):
    """Decorator for Flask routes"""
    from functools import wraps
    from flask import request, jsonify
    
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Get client IP
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if ',' in ip:
                ip = ip.split(',')[0].strip()
            
            # Check rate limit
            result = limiter.check_rate_limit(ip, is_download=is_download)
            
            if not result['allowed']:
                return jsonify({
                    'success': False,
                    'error': result['reason'],
                    'retry_after': result['retry_after']
                }), 429  # Too Many Requests
            
            return f(*args, **kwargs)
        return wrapped
    return decorator


# Usage example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    limiter = RateLimiter(
        max_requests_per_minute=10,
        max_requests_per_hour=100,
        max_downloads_per_day=500
    )
    
    limiter.start_background_cleanup()
    
    # Test
    test_ip = "192.168.1.100"
    
    for i in range(15):
        result = limiter.check_rate_limit(test_ip, is_download=True)
        print(f"Request {i+1}: {result}")
        
        if not result['allowed']:
            break
    
    stats = limiter.get_stats(test_ip)
    print(f"\nStats: {stats}")
    
    global_stats = limiter.get_all_stats()
    print(f"Global Stats: {global_stats}")
