#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Downloader - Web Application (v2.0)
Complete rewrite with saveclip.app feature parity
"""

import os
import sys
import json
import time
import uuid
import threading
import re
import logging
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import quote
from flask import Flask, render_template, request, jsonify, send_file, Response
import zipfile

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from main import InstagramDownloaderConfig, SessionManager
from downloader import InstagramDownloader
from cleanup_manager import StorageCleanupManager
from rate_limiter import RateLimiter, rate_limit_decorator

# Flask app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

# Paths configuration
BASE_DIR = Path(__file__).parent.parent
DOWNLOADS_DIR = BASE_DIR / "downloads"
TEMP_DIR = BASE_DIR / "temp_zips"

# Create folders
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global state
download_jobs = {}
session_manager = None
loader = None
downloader = None

# Storage cleanup manager (initialized after DOWNLOADS_DIR is defined)
cleanup_manager = None

# Rate limiter
rate_limiter = RateLimiter(
    max_requests_per_minute=int(os.environ.get('RATE_LIMIT_PER_MINUTE', 10)),
    max_requests_per_hour=int(os.environ.get('RATE_LIMIT_PER_HOUR', 100)),
    max_downloads_per_day=int(os.environ.get('RATE_LIMIT_PER_DAY', 500)),
    cooldown_after_ban=int(os.environ.get('BAN_COOLDOWN_SECONDS', 3600))
)


class DownloadJob:
    """Enhanced download job tracker"""
    
    def __init__(self, job_id: str, job_type: str, target: str):
        self.job_id = job_id
        self.job_type = job_type  # 'profile', 'post', 'reel', 'story', 'profile_pic', 'batch'
        self.target = target  # username or shortcode
        self.status = 'pending'  # pending, running, completed, failed
        self.progress = 0  # 0-100
        self.created_at = datetime.now()
        self.completed_at = None
        self.error_message = None
        self.download_path = None
        
        # Detailed progress
        self.total_items = 0
        self.downloaded_items = 0
        self.failed_items = 0
        self.current_item_name = None
        self.phase = 'initializing'  # initializing, downloading, completed, failed
        
        # Results
        self.results = {}
        
    def to_dict(self):
        return {
            'job_id': self.job_id,
            'job_type': self.job_type,
            'target': self.target,
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'download_path': self.download_path,
            'total_items': self.total_items,
            'downloaded_items': self.downloaded_items,
            'failed_items': self.failed_items,
            'current_item_name': self.current_item_name,
            'phase': self.phase,
            'results': self.results
        }


def parse_instagram_url(url_or_username: str) -> dict:
    """Parse Instagram URL or username
    
    Supports:
    - Username: cristiano
    - Profile URL: https://www.instagram.com/cristiano/
    - Post URL: https://www.instagram.com/p/ABC123/
    - Reel URL: https://www.instagram.com/reel/ABC123/
    - Story URL: https://www.instagram.com/stories/username/123456789/
    - IGTV URL: https://www.instagram.com/tv/ABC123/
    
    Returns:
        dict: {'type': str, 'identifier': str, 'username': str}
    """
    url_or_username = url_or_username.strip()
    
    # If it's just a username
    if not url_or_username.startswith('http'):
        username = url_or_username.lstrip('@')
        return {'type': 'profile', 'identifier': username, 'username': username}
    
    # Parse URL patterns
    patterns = {
        'post': r'instagram\.com/p/([A-Za-z0-9_-]+)',
        'reel': r'instagram\.com/(?:reel|reels)/([A-Za-z0-9_-]+)',
        'igtv': r'instagram\.com/tv/([A-Za-z0-9_-]+)',
        'story': r'instagram\.com/stories/([^/]+)/([0-9]+)',
        'profile': r'instagram\.com/([A-Za-z0-9_.]+)/?$'
    }
    
    for content_type, pattern in patterns.items():
        match = re.search(pattern, url_or_username)
        if match:
            if content_type == 'story':
                return {
                    'type': 'story',
                    'identifier': match.group(2),
                    'username': match.group(1)
                }
            elif content_type == 'profile':
                username = match.group(1)
                # Exclude common paths
                if username not in ['p', 'reel', 'reels', 'tv', 'stories', 'explore']:
                    return {'type': 'profile', 'identifier': username, 'username': username}
            else:
                return {
                    'type': content_type,
                    'identifier': match.group(1),
                    'username': None
                }
    
    # Default: treat as username
    username = url_or_username.split('/')[-1].split('?')[0].lstrip('@')
    return {'type': 'profile', 'identifier': username, 'username': username}


def initialize_downloader():
    """Initialize Instagram downloader"""
    global session_manager, loader, downloader, cleanup_manager
    
    try:
        config = InstagramDownloaderConfig()
        session_manager = SessionManager()
        loader = session_manager.load_or_create()
        downloader = InstagramDownloader(loader)
        
        # Initialize cleanup manager with DISABLED auto-cleanup (set age to 365 days)
        cleanup_manager = StorageCleanupManager(
            download_folder=DOWNLOADS_DIR,
            max_age_hours=int(os.environ.get('DOWNLOAD_TTL_HOURS', 8760)),  # 365 days default
            max_storage_mb=int(os.environ.get('MAX_STORAGE_MB', 50000)),  # 50GB default
            cleanup_interval_seconds=int(os.environ.get('CLEANUP_INTERVAL', 86400))  # Daily check
        )
        
        # DO NOT start automatic cleanup - manual only
        # cleanup_manager.start_background_cleanup()
        rate_limiter.start_background_cleanup()
        
        logger.info("Initialized downloader (cleanup DISABLED for safety)")
        return True
    except Exception as e:
        logger.error(f"Initialization error: {e}")
        return False


def cleanup_old_jobs():
    """Remove completed jobs older than 1 hour"""
    global download_jobs
    now = datetime.now()
    
    jobs_to_remove = []
    for job_id, job in download_jobs.items():
        if job.status in ['completed', 'failed']:
            if job.completed_at and (now - job.completed_at).total_seconds() > 3600:
                jobs_to_remove.append(job_id)
    
    for job_id in jobs_to_remove:
        del download_jobs[job_id]
        logger.info(f"Removed old job: {job_id}")
    
    return len(jobs_to_remove)


# ==== DOWNLOAD TASKS ====

def download_profile_pic_task(job: DownloadJob, username: str):
    """Download only profile picture"""
    try:
        job.status = 'running'
        job.phase = 'downloading'
        job.total_items = 1
        
        download_dir = DOWNLOADS_DIR / username
        result = downloader.download_profile_picture(username, download_dir)
        
        if result['success']:
            job.downloaded_items = 1
            job.progress = 100
            job.status = 'completed'
            job.phase = 'completed'
            job.download_path = str(download_dir / "profile_picture")
            job.results = {'profile_pic': result}
        else:
            job.status = 'failed'
            job.phase = 'failed'
            job.error_message = result.get('error', 'Unknown error')
            job.failed_items = 1
        
        job.completed_at = datetime.now()
        logger.info(f"Profile pic download completed for {username}: {result}")
        
    except Exception as e:
        logger.error(f"Profile pic download failed for {username}: {e}")
        job.status = 'failed'
        job.phase = 'failed'
        job.error_message = str(e)
        job.completed_at = datetime.now()


def download_story_task(job: DownloadJob, username: str):
    """Download stories only"""
    try:
        job.status = 'running'
        job.phase = 'downloading'
        
        download_dir = DOWNLOADS_DIR / username
        result = downloader.download_stories(username, download_dir)
        
        job.total_items = result.get('downloaded', 0) + result.get('failed', 0)
        job.downloaded_items = result.get('downloaded', 0)
        job.failed_items = result.get('failed', 0)
        
        if result['success']:
            job.progress = 100
            job.status = 'completed'
            job.phase = 'completed'
            job.download_path = str(download_dir / "stories")
        else:
            job.status = 'failed'
            job.phase = 'failed'
            job.error_message = result.get('error', 'No stories available')
        
        job.results = {'stories': result}
        job.completed_at = datetime.now()
        logger.info(f"Story download completed for {username}: {result}")
        
    except Exception as e:
        logger.error(f"Story download failed for {username}: {e}")
        job.status = 'failed'
        job.phase = 'failed'
        job.error_message = str(e)
        job.completed_at = datetime.now()


def download_single_post_task(job: DownloadJob, shortcode: str, content_type: str = 'post'):
    """Download single post/reel/IGTV"""
    try:
        job.status = 'running'
        job.phase = 'downloading'
        job.total_items = 1
        
        download_dir = DOWNLOADS_DIR
        result = downloader.download_single_post(shortcode, download_dir)
        
        if result['success']:
            job.downloaded_items = 1
            job.progress = 100
            job.status = 'completed'
            job.phase = 'completed'
            job.download_path = result['path']
            job.results = {content_type: result}
        else:
            job.status = 'failed'
            job.phase = 'failed'
            job.error_message = result.get('error', 'Unknown error')
            job.failed_items = 1
        
        job.completed_at = datetime.now()
        logger.info(f"Single {content_type} download completed for {shortcode}: {result}")
        
    except Exception as e:
        logger.error(f"Single {content_type} download failed for {shortcode}: {e}")
        job.status = 'failed'
        job.phase = 'failed'
        job.error_message = str(e)
        job.completed_at = datetime.now()


def download_full_profile_task(job: DownloadJob, username: str, max_posts: int = None, 
                                download_profile_pic: bool = True,
                                download_stories: bool = False,
                                download_highlights: bool = False):
    """Download complete profile with all options"""
    try:
        job.status = 'running'
        job.phase = 'initializing'
        
        download_dir = DOWNLOADS_DIR / username
        download_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        # 1. Profile Picture
        if download_profile_pic:
            job.phase = 'downloading_profile_pic'
            job.current_item_name = 'Profile Picture'
            result = downloader.download_profile_picture(username, download_dir)
            results['profile_pic'] = result
            if result['success']:
                job.downloaded_items += 1
        
        # 2. Stories
        if download_stories:
            job.phase = 'downloading_stories'
            job.current_item_name = 'Stories'
            result = downloader.download_stories(username, download_dir)
            results['stories'] = result
            if result['success']:
                job.downloaded_items += result.get('downloaded', 0)
                job.failed_items += result.get('failed', 0)
        
        # 3. Highlights
        if download_highlights:
            job.phase = 'downloading_highlights'
            job.current_item_name = 'Highlights'
            result = downloader.download_highlights(username, download_dir)
            results['highlights'] = result
            if result['success']:
                job.downloaded_items += result.get('downloaded', 0)
                job.failed_items += result.get('failed', 0)
        
        # 4. Posts
        job.phase = 'downloading_posts'
        job.current_item_name = 'Posts'
        result = downloader.download_posts(username, download_dir, max_posts)
        results['posts'] = result
        
        if result['success']:
            job.total_items = result['total_available']
            job.downloaded_items += result['total_downloaded']
            job.failed_items += result['failed']
        
        # Save metadata
        metadata = {
            'username': username,
            'download_timestamp': datetime.now().isoformat(),
            'results': results,
            'total_downloaded': job.downloaded_items,
            'total_failed': job.failed_items
        }
        
        with open(download_dir / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Complete
        job.progress = 100
        job.status = 'completed'
        job.phase = 'completed'
        job.download_path = str(download_dir)
        job.results = results
        job.completed_at = datetime.now()
        
        logger.info(f"Full profile download completed for {username}")
        
    except Exception as e:
        logger.error(f"Full profile download failed for {username}: {e}")
        job.status = 'failed'
        job.phase = 'failed'
        job.error_message = str(e)
        job.completed_at = datetime.now()


# ==== API ROUTES ====

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/download', methods=['POST'])
@rate_limit_decorator(rate_limiter, is_download=True)
def download():
    """Universal download endpoint"""
    try:
        # Cleanup old jobs periodically
        cleanup_old_jobs()
        
        data = request.get_json()
        input_value = data.get('url', '').strip()
        download_type = data.get('type', 'auto')  # auto, profile, post, reel, story, profile_pic
        max_posts = data.get('max_posts')
        download_profile_pic = data.get('download_profile_pic', True)
        download_stories = data.get('download_stories', False)
        download_highlights = data.get('download_highlights', False)
        
        if not input_value:
            return jsonify({'error': 'URL or username is required'}), 400
        
        # Parse input
        parsed = parse_instagram_url(input_value)
        
        # Override type if specified
        if download_type != 'auto':
            parsed['type'] = download_type
        
        content_type = parsed['type']
        identifier = parsed['identifier']
        username = parsed.get('username') or identifier
        
        # Convert max_posts
        if max_posts:
            try:
                max_posts = int(max_posts)
            except (ValueError, TypeError):
                max_posts = None
        
        logger.info(f"Download request: type={content_type}, identifier={identifier}, max_posts={max_posts}")
        
        # Create job
        job_id = str(uuid.uuid4())
        job = DownloadJob(job_id, content_type, identifier)
        download_jobs[job_id] = job
        
        # Start appropriate download task
        if content_type == 'profile_pic':
            thread = threading.Thread(target=download_profile_pic_task, args=(job, username))
            message = f'Profile picture download started for {username}'
            
        elif content_type == 'story':
            thread = threading.Thread(target=download_story_task, args=(job, username))
            message = f'Stories download started for {username}'
            
        elif content_type in ['post', 'reel', 'igtv']:
            thread = threading.Thread(target=download_single_post_task, args=(job, identifier, content_type))
            message = f'{content_type.capitalize()} download started'
            
        else:  # Full profile
            thread = threading.Thread(
                target=download_full_profile_task,
                args=(job, username, max_posts, download_profile_pic, download_stories, download_highlights)
            )
            message = f'Profile download started for {username}'
        
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'content_type': content_type,
            'identifier': identifier,
            'message': message
        })
        
    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get job status"""
    job = download_jobs.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job.to_dict())


@app.route('/api/image-proxy')
def image_proxy():
    """Proxy Instagram images to bypass CORS"""
    try:
        image_url = request.args.get('url')
        if not image_url:
            return jsonify({'error': 'URL parameter required'}), 400
        
        # Fetch image from Instagram
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.instagram.com/',
        }
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Return image with proper headers
        return Response(
            response.content,
            mimetype=response.headers.get('Content-Type', 'image/jpeg'),
            headers={
                'Cache-Control': 'public, max-age=3600',
                'Access-Control-Allow-Origin': '*'
            }
        )
    except Exception as e:
        logger.error(f"Image proxy error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/preview', methods=['POST'])
def get_preview():
    """Get preview of profile content with thumbnails"""
    try:
        data = request.get_json()
        input_value = data.get('url', '').strip()
        max_items = data.get('max_items', 25)
        
        if not input_value:
            return jsonify({'error': 'URL or username is required'}), 400
        
        # Parse input
        parsed = parse_instagram_url(input_value)
        username = parsed.get('username') or parsed['identifier']
        
        logger.info(f"Preview request for {username}, max {max_items} items")
        
        # Get preview
        preview = downloader.get_profile_preview(username, max_items)
        
        if preview['success']:
            # Replace thumbnail URLs with proxy URLs
            for item in preview.get('preview_items', []):
                if item.get('thumbnail_url'):
                    original_url = item['thumbnail_url']
                    item['thumbnail_url'] = f"/api/image-proxy?url={quote(original_url)}"
                if item.get('display_url'):
                    original_url = item['display_url']
                    item['display_url'] = f"/api/image-proxy?url={quote(original_url)}"
            
            return jsonify(preview)
        else:
            return jsonify({'error': preview.get('error', 'Failed to fetch preview')}), 500
            
    except Exception as e:
        logger.error(f"Preview error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/selected', methods=['POST'])
@rate_limit_decorator(rate_limiter, is_download=True)
def download_selected():
    """Download only selected posts"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        shortcodes = data.get('shortcodes', [])
        
        if not username or not shortcodes:
            return jsonify({'error': 'Username and shortcodes are required'}), 400
        
        logger.info(f"Selected download: {username}, {len(shortcodes)} items")
        
        # Create job
        job_id = str(uuid.uuid4())
        job = DownloadJob(job_id, 'selected', username)
        job.total_items = len(shortcodes)
        download_jobs[job_id] = job
        
        # Start download in background
        def download_selected_task():
            try:
                job.status = 'running'
                job.phase = 'downloading'
                
                # Progress callback to update job in real-time
                def update_progress(current, total, shortcode):
                    job.downloaded_items = current
                    job.progress = int((current / total) * 100)
                    job.current_item_name = shortcode
                    logger.debug(f"Progress: {current}/{total} ({job.progress}%) - {shortcode}")
                
                download_dir = Path("downloads")
                result = downloader.download_selected_posts(username, shortcodes, download_dir, progress_callback=update_progress)
                
                if result['success']:
                    job.downloaded_items = result['downloaded_count']
                    job.failed_items = result['failed_count']
                    job.progress = 100
                    job.status = 'completed'
                    job.phase = 'completed'
                    job.download_path = result['download_path']
                    job.results = result
                else:
                    job.status = 'failed'
                    job.phase = 'failed'
                    job.error_message = result.get('error', 'Unknown error')
                
                job.completed_at = datetime.now()
                logger.info(f"Selected download completed: {result}")
                
            except Exception as e:
                logger.error(f"Selected download failed: {e}")
                job.status = 'failed'
                job.phase = 'failed'
                job.error_message = str(e)
                job.completed_at = datetime.now()
        
        thread = threading.Thread(target=download_selected_task)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': f'Downloading {len(shortcodes)} selected items from {username}'
        })
        
    except Exception as e:
        logger.error(f"Selected download error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs', methods=['GET'])
def get_all_jobs():
    """Get all jobs"""
    return jsonify([job.to_dict() for job in download_jobs.values()])


@app.route('/api/profiles/list', methods=['GET'])
def list_profiles():
    """List all downloaded profiles with accurate counts"""
    try:
        downloads_dir = DOWNLOADS_DIR
        
        if not downloads_dir.exists():
            return jsonify([])
        
        profiles = []
        for profile_dir in downloads_dir.iterdir():
            if profile_dir.is_dir() and not profile_dir.name.startswith('.'):
                # Use accurate counting
                counts = downloader.count_downloaded_media(profile_dir)
                
                # Get metadata
                metadata_file = profile_dir / "metadata.json"
                metadata = {}
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                    except:
                        pass
                
                profiles.append({
                    'username': profile_dir.name,
                    'photo_count': counts['photos'],
                    'video_count': counts['videos'],
                    'total_count': counts['total'],
                    'path': str(profile_dir),
                    'metadata': metadata
                })
        
        return jsonify(profiles)
        
    except Exception as e:
        logger.error(f"Error listing profiles: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/zip/<path:folder>', methods=['GET'])
def download_zip(folder):
    """Create and download ZIP of a folder"""
    try:
        # Sanitize folder name
        folder = folder.replace('..', '').strip('/')
        folder_path = DOWNLOADS_DIR / folder
        
        if not folder_path.exists():
            logger.error(f"Folder not found: {folder_path}")
            return jsonify({'error': f'Folder not found: {folder}'}), 404
        
        # Create ZIP in temp directory
        zip_filename = f"{folder}_{int(time.time())}.zip"
        zip_path = TEMP_DIR / zip_filename
        
        logger.info(f"Creating ZIP: {zip_path} from {folder_path}")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = Path(root) / file
                    # Use relative path in ZIP
                    arcname = file_path.relative_to(folder_path.parent)
                    zipf.write(file_path, arcname)
                    logger.info(f"Added to ZIP: {arcname}")
        
        # Check if ZIP was created
        if not zip_path.exists():
            logger.error(f"ZIP file was not created: {zip_path}")
            return jsonify({'error': 'Failed to create ZIP file'}), 500
        
        logger.info(f"ZIP created successfully: {zip_path} ({zip_path.stat().st_size} bytes)")
        
        # Send file
        response = send_file(
            zip_path, 
            as_attachment=True,
            download_name=f"{folder}.zip",
            mimetype='application/zip'
        )
        
        # Schedule ZIP deletion after 1 minute (cleanup old temp files)
        def cleanup_temp_zip():
            try:
                time.sleep(60)  # Wait 1 minute
                if zip_path.exists():
                    zip_path.unlink()
                    logger.info(f"Cleaned up temp ZIP: {zip_path}")
            except Exception as e:
                logger.error(f"Error cleaning temp ZIP: {e}")
        
        threading.Thread(target=cleanup_temp_zip, daemon=True).start()
        
        return response
        
    except Exception as e:
        logger.error(f"ZIP download error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'features': [
            'profile_pictures',
            'stories',
            'highlights',
            'posts',
            'reels',
            'igtv',
            'accurate_counting'
        ]
    })


@app.route('/api/stats/storage', methods=['GET'])
def storage_stats():
    """Get storage statistics"""
    try:
        stats = cleanup_manager.get_storage_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats/rate-limit', methods=['GET'])
def rate_limit_stats():
    """Get rate limiting statistics"""
    try:
        # Get client IP
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ',' in ip:
            ip = ip.split(',')[0].strip()
        
        user_stats = rate_limiter.get_stats(ip)
        global_stats = rate_limiter.get_all_stats()
        
        return jsonify({
            'success': True,
            'your_stats': user_stats,
            'global_stats': global_stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/cleanup', methods=['POST'])
def manual_cleanup():
    """Manually trigger cleanup (admin only)"""
    try:
        # Add authentication here in production
        result = cleanup_manager.perform_cleanup()
        job_cleanup_count = cleanup_old_jobs()
        
        return jsonify({
            'success': True,
            'storage_cleanup': result,
            'jobs_cleaned': job_cleanup_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Instagram Downloader v2.0 - Web Interface")
    print("="*60)
    print("\nInitializing...")
    
    if initialize_downloader():
        print("✅ Downloader initialized successfully")
        print("\n🎯 Features:")
        print("  ✓ Profile Pictures (HD)")
        print("  ✓ Stories")
        print("  ✓ Highlights")
        print("  ✓ Posts, Reels, IGTV")
        print("  ✓ Accurate file counting")
        print("  ✓ URL parsing")
        print("\nStarting web server...")
        print("🌐 Open browser: http://localhost:5000")
        print("\nPress Ctrl+C to stop")
        print("="*60 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    else:
        print("❌ Failed to initialize downloader")
        sys.exit(1)
