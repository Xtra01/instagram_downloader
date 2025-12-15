#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Production Configuration Helper
Automatically generates optimized .env file based on server specs
"""

import os
import psutil
import sys
from pathlib import Path


def get_system_specs():
    """Detect system resources"""
    return {
        'cpu_count': psutil.cpu_count(),
        'total_ram_mb': psutil.virtual_memory().total / (1024 * 1024),
        'available_ram_mb': psutil.virtual_memory().available / (1024 * 1024),
        'total_disk_gb': psutil.disk_usage('/').total / (1024 * 1024 * 1024),
        'free_disk_gb': psutil.disk_usage('/').free / (1024 * 1024 * 1024)
    }


def recommend_settings(specs):
    """Recommend optimal settings based on system specs"""
    ram = specs['total_ram_mb']
    disk = specs['free_disk_gb']
    
    # Conservative recommendations
    if ram < 512:
        # Very limited RAM (shared hosting)
        return {
            'MAX_STORAGE_MB': min(int(disk * 1024 * 0.3), 2000),  # 30% of disk or 2GB
            'RATE_LIMIT_PER_MINUTE': 5,
            'RATE_LIMIT_PER_HOUR': 50,
            'RATE_LIMIT_PER_DAY': 200,
            'DOWNLOAD_TTL_HOURS': 12,
            'CLEANUP_INTERVAL': 1800,  # 30 minutes
            'GUNICORN_WORKERS': 2,
            'note': 'Low resource mode - Shared hosting'
        }
    elif ram < 1024:
        # 512 MB - 1 GB RAM (small VPS)
        return {
            'MAX_STORAGE_MB': min(int(disk * 1024 * 0.4), 5000),  # 40% of disk or 5GB
            'RATE_LIMIT_PER_MINUTE': 10,
            'RATE_LIMIT_PER_HOUR': 100,
            'RATE_LIMIT_PER_DAY': 500,
            'DOWNLOAD_TTL_HOURS': 24,
            'CLEANUP_INTERVAL': 3600,  # 1 hour
            'GUNICORN_WORKERS': 3,
            'note': 'Standard mode - Small VPS'
        }
    elif ram < 2048:
        # 1-2 GB RAM (medium VPS)
        return {
            'MAX_STORAGE_MB': min(int(disk * 1024 * 0.5), 10000),  # 50% of disk or 10GB
            'RATE_LIMIT_PER_MINUTE': 15,
            'RATE_LIMIT_PER_HOUR': 150,
            'RATE_LIMIT_PER_DAY': 1000,
            'DOWNLOAD_TTL_HOURS': 24,
            'CLEANUP_INTERVAL': 3600,
            'GUNICORN_WORKERS': 4,
            'note': 'Medium mode - Medium VPS'
        }
    else:
        # 2+ GB RAM (large VPS)
        return {
            'MAX_STORAGE_MB': min(int(disk * 1024 * 0.6), 20000),  # 60% of disk or 20GB
            'RATE_LIMIT_PER_MINUTE': 20,
            'RATE_LIMIT_PER_HOUR': 200,
            'RATE_LIMIT_PER_DAY': 2000,
            'DOWNLOAD_TTL_HOURS': 24,
            'CLEANUP_INTERVAL': 7200,  # 2 hours
            'GUNICORN_WORKERS': min(specs['cpu_count'] * 2, 8),
            'note': 'High performance mode - Large VPS'
        }


def generate_env_file(settings, output_path='.env'):
    """Generate .env file with recommended settings"""
    import secrets
    
    secret_key = secrets.token_hex(32)
    
    env_content = f"""# Instagram Downloader - Production Configuration
# Auto-generated based on system specs: {settings['note']}

# ==== Flask Configuration ====
SECRET_KEY={secret_key}
FLASK_ENV=production
FLASK_DEBUG=0

# ==== Server Configuration ====
PORT=5000
HOST=0.0.0.0

# ==== Storage Management ====
DOWNLOAD_TTL_HOURS={settings['DOWNLOAD_TTL_HOURS']}
MAX_STORAGE_MB={settings['MAX_STORAGE_MB']}
CLEANUP_INTERVAL={settings['CLEANUP_INTERVAL']}

# ==== Rate Limiting ====
RATE_LIMIT_PER_MINUTE={settings['RATE_LIMIT_PER_MINUTE']}
RATE_LIMIT_PER_HOUR={settings['RATE_LIMIT_PER_HOUR']}
RATE_LIMIT_PER_DAY={settings['RATE_LIMIT_PER_DAY']}
BAN_COOLDOWN_SECONDS=3600

# ==== Instagram API Settings ====
MAX_POSTS_PER_PROFILE=50
INSTAGRAM_REQUEST_DELAY=3
DOWNLOAD_TIMEOUT=300

# ==== File Settings ====
MAX_FILE_SIZE=104857600

# ==== Production Notes ====
# System Specs Detected:
# - Configuration: {settings['note']}
# - Recommended Gunicorn workers: {settings['GUNICORN_WORKERS']}
#
# To start with Gunicorn:
# gunicorn -w {settings['GUNICORN_WORKERS']} -b 0.0.0.0:5000 --timeout 300 web.app:app
"""
    
    with open(output_path, 'w') as f:
        f.write(env_content)
    
    return output_path


def main():
    print("🔍 Detecting system specifications...")
    specs = get_system_specs()
    
    print(f"\n📊 System Specs:")
    print(f"  CPU Cores: {specs['cpu_count']}")
    print(f"  Total RAM: {specs['total_ram_mb']:.0f} MB")
    print(f"  Available RAM: {specs['available_ram_mb']:.0f} MB")
    print(f"  Total Disk: {specs['total_disk_gb']:.1f} GB")
    print(f"  Free Disk: {specs['free_disk_gb']:.1f} GB")
    
    print("\n⚙️  Calculating optimal settings...")
    settings = recommend_settings(specs)
    
    print(f"\n✅ Recommended Configuration ({settings['note']}):")
    print(f"  Max Storage: {settings['MAX_STORAGE_MB']} MB")
    print(f"  Rate Limit (per minute): {settings['RATE_LIMIT_PER_MINUTE']}")
    print(f"  Rate Limit (per hour): {settings['RATE_LIMIT_PER_HOUR']}")
    print(f"  Rate Limit (per day): {settings['RATE_LIMIT_PER_DAY']}")
    print(f"  File TTL: {settings['DOWNLOAD_TTL_HOURS']} hours")
    print(f"  Cleanup Interval: {settings['CLEANUP_INTERVAL']} seconds")
    print(f"  Gunicorn Workers: {settings['GUNICORN_WORKERS']}")
    
    # Ask user
    response = input("\n📝 Generate .env file with these settings? (y/n): ").lower()
    
    if response == 'y':
        env_path = generate_env_file(settings)
        print(f"\n✅ Generated: {env_path}")
        print("\n🎯 Next steps:")
        print("  1. Review and edit .env file if needed")
        print(f"  2. Start server: gunicorn -w {settings['GUNICORN_WORKERS']} -b 0.0.0.0:5000 --timeout 300 web.app:app")
        print("  3. Setup Nginx as reverse proxy (see docs/WEB_DEPLOYMENT.md)")
        print("  4. Configure SSL with Let's Encrypt")
    else:
        print("\n❌ Cancelled. You can manually create .env file using .env.example")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
