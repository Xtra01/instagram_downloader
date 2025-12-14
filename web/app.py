#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Downloader - Web Application
Flask-based web interface for Instagram profile downloading
"""

import os
import sys
import json
import time
import uuid
import threading
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
import zipfile
import shutil
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import (
    InstagramDownloaderConfig,
    SessionManager,
    InstagramProfileDownloader
)
from advanced import InstagramAPIWrapper

# Flask app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'instagram-downloader-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max
app.config['DOWNLOAD_FOLDER'] = Path(__file__).parent / 'static' / 'downloads'
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / 'static' / 'uploads'

# Create folders
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global state
download_jobs = {}  # {job_id: {...job_info...}}
session_manager = None
loader = None
config = None
logger = logging.getLogger(__name__)


class DownloadJob:
    """Download job tracker with detailed progress"""
    
    def __init__(self, job_id: str, job_type: str, profiles: List[str]):
        self.job_id = job_id
        self.job_type = job_type  # 'single' or 'batch'
        self.profiles = profiles
        self.status = 'pending'  # pending, running, completed, failed
        self.progress = 0  # 0-100
        self.current_profile = None
        self.completed_profiles = []
        self.failed_profiles = []
        self.created_at = datetime.now()
        self.completed_at = None
        self.error_message = None
        self.download_paths = []
        
        # Detailed progress tracking
        self.total_items = 0  # Total media items to download
        self.current_item = 0  # Current item being downloaded
        self.downloaded_items = 0  # Successfully downloaded
        self.failed_items = 0  # Failed downloads
        self.current_item_name = None  # Current file name
        self.estimated_items = None  # Estimated total (before exact count)
        self.phase = 'initializing'  # initializing, counting, downloading, completed
        
    def to_dict(self):
        return {
            'job_id': self.job_id,
            'job_type': self.job_type,
            'profiles': self.profiles,
            'status': self.status,
            'progress': self.progress,
            'current_profile': self.current_profile,
            'completed_profiles': self.completed_profiles,
            'failed_profiles': self.failed_profiles,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'download_paths': self.download_paths,
            # Detailed progress
            'total_items': self.total_items,
            'current_item': self.current_item,
            'downloaded_items': self.downloaded_items,
            'failed_items': self.failed_items,
            'current_item_name': self.current_item_name,
            'estimated_items': self.estimated_items,
            'phase': self.phase,
            'remaining_items': self.total_items - self.downloaded_items - self.failed_items if self.total_items > 0 else 0
        }


def parse_instagram_url(url_or_username: str) -> dict:
    """Parse Instagram URL or username and return type and identifier.
    
    Supports:
    - Username: cristiano
    - Profile URL: https://www.instagram.com/cristiano/
    - Post URL: https://www.instagram.com/p/ABC123/
    - Reel URL: https://www.instagram.com/reel/ABC123/
    - Story URL: https://www.instagram.com/stories/username/123456789/
    - IGTV URL: https://www.instagram.com/tv/ABC123/
    
    Returns:
        dict: {'type': 'profile'|'post'|'reel'|'story'|'igtv', 'identifier': str, 'username': str}
    """
    url_or_username = url_or_username.strip()
    
    # If it's just a username (no URL)
    if not url_or_username.startswith('http'):
        # Remove @ if present
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
                    'username': None  # Will be fetched from post
                }
    
    # Default: treat as username
    username = url_or_username.split('/')[-1].split('?')[0].lstrip('@')
    return {'type': 'profile', 'identifier': username, 'username': username}


def initialize_downloader():
    """Initialize Instagram downloader"""
    global session_manager, loader, config
    
    try:
        config = InstagramDownloaderConfig()
        session_manager = SessionManager()
        loader = session_manager.load_or_create()
        return True
    except Exception as e:
        print(f"Initialization error: {e}")
        return False


def download_profile_task(job: DownloadJob, username: str, max_posts: int = None):
    """Download a single profile with detailed progress tracking and proper max_posts limit"""
    from instaloader import Profile
    
    try:
        job.status = 'running'
        job.current_profile = username
        job.phase = 'initializing'
        logger.info(f"Starting download for {username}, max_posts={max_posts}")
        
        # Load profile and get total post count
        job.phase = 'counting'
        try:
            profile = Profile.from_username(loader.context, username)
            
            # Calculate total items to download
            if max_posts and max_posts > 0:
                job.total_items = min(profile.mediacount, max_posts)
            else:
                job.total_items = profile.mediacount
            
            job.estimated_items = job.total_items
            logger.info(f"Profile {username} has {profile.mediacount} posts. Will download {job.total_items}.")
            
        except Exception as e:
            logger.error(f"Failed to load profile {username}: {e}")
            raise
        
        # Start downloading with manual iteration
        job.phase = 'downloading'
        
        # Create download directory
        download_dir = Path("downloads") / username
        download_dir.mkdir(parents=True, exist_ok=True)
        
        # Download posts manually with proper limit
        downloaded_count = 0
        for post in profile.get_posts():
            # Check limit
            if max_posts and downloaded_count >= max_posts:
                logger.info(f"Reached max_posts limit of {max_posts}. Stopping.")
                break
            
            try:
                # Download post
                loader.download_post(post, target=str(download_dir))
                downloaded_count += 1
                job.downloaded_items = downloaded_count
                job.current_item = downloaded_count
                
                # Update progress
                if job.total_items > 0:
                    job.progress = int((job.downloaded_items / job.total_items) * 100)
                
                logger.info(f"Downloaded {downloaded_count}/{job.total_items} posts ({job.progress}%)")
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Failed to download post {post.shortcode}: {e}")
                job.failed_items += 1
                # Continue with next post
                continue
        
        # Save profile metadata
        metadata = {
            "username": profile.username,
            "full_name": profile.full_name,
            "biography": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "total_posts": profile.mediacount,
            "downloaded_posts": downloaded_count,
            "is_private": profile.is_private,
            "download_timestamp": datetime.now().isoformat()
        }
        
        metadata_file = download_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Mark as completed
        job.download_paths.append(str(download_dir))
        job.completed_profiles.append(username)
        job.phase = 'completed'
        
        # Update overall progress
        if job.job_type == 'batch':
            completed_count = len(job.completed_profiles) + len(job.failed_profiles)
            job.progress = int((completed_count / len(job.profiles)) * 100)
        else:
            job.progress = 100
            job.status = 'completed'
            job.completed_at = datetime.now()
        
        logger.info(f"Successfully downloaded {downloaded_count} posts from {username}")
        
    except Exception as e:
        logger.error(f"Error downloading {username}: {e}")
        job.failed_profiles.append({'username': username, 'error': str(e)})
        job.failed_items += 1
        job.phase = 'failed'
        
        if job.job_type == 'single':
            job.status = 'failed'
            job.error_message = str(e)
            job.completed_at = datetime.now()
        else:
            # For batch, update progress
            completed_count = len(job.completed_profiles) + len(job.failed_profiles)
            job.progress = int((completed_count / len(job.profiles)) * 100)


def download_single_post_task(job: DownloadJob, shortcode: str, content_type: str = 'post'):
    """Download a single post, reel, or IGTV video"""
    from instaloader import Post
    
    try:
        job.status = 'running'
        job.phase = 'initializing'
        job.total_items = 1
        job.estimated_items = 1
        
        logger.info(f"Downloading single {content_type}: {shortcode}")
        
        # Load post
        job.phase = 'downloading'
        post = Post.from_shortcode(loader.context, shortcode)
        
        # Get username and create directory
        username = post.owner_username
        job.current_profile = username
        
        download_dir = Path("downloads") / f"{username}_{content_type}_{shortcode}"
        download_dir.mkdir(parents=True, exist_ok=True)
        
        # Download the post
        loader.download_post(post, target=str(download_dir))
        
        # Save metadata
        metadata = {
            "shortcode": shortcode,
            "type": content_type,
            "owner_username": username,
            "caption": post.caption if post.caption else "",
            "likes": post.likes,
            "comments": post.comments,
            "is_video": post.is_video,
            "url": f"https://www.instagram.com/p/{shortcode}/",
            "download_timestamp": datetime.now().isoformat()
        }
        
        metadata_file = download_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Update job
        job.downloaded_items = 1
        job.current_item = 1
        job.progress = 100
        job.download_paths.append(str(download_dir))
        job.completed_profiles.append(f"{username}/{shortcode}")
        job.phase = 'completed'
        job.status = 'completed'
        job.completed_at = datetime.now()
        
        logger.info(f"Successfully downloaded {content_type} {shortcode}")
        
    except Exception as e:
        logger.error(f"Error downloading {content_type} {shortcode}: {e}")
        job.failed_profiles.append({'shortcode': shortcode, 'error': str(e)})
        job.failed_items = 1
        job.phase = 'failed'
        job.status = 'failed'
        job.error_message = str(e)
        job.completed_at = datetime.now()


def download_batch_task(job: DownloadJob, max_posts: int = None):
    """Download multiple profiles (runs in thread)"""
    try:
        job.status = 'running'
        
        for i, username in enumerate(job.profiles):
            job.current_profile = username
            download_profile_task(job, username, max_posts)
            
            # Delay between profiles
            if i < len(job.profiles) - 1:
                time.sleep(3)
        
        job.status = 'completed'
        job.completed_at = datetime.now()
        
    except Exception as e:
        job.status = 'failed'
        job.error_message = str(e)
        job.completed_at = datetime.now()


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/download/single', methods=['POST'])
def download_single():
    """Download single profile, post, reel, or IGTV - supports URLs"""
    try:
        data = request.get_json()
        input_value = data.get('username', '').strip()  # Can be username or URL
        max_posts = data.get('max_posts')
        
        if not input_value:
            return jsonify({'error': 'Username or URL is required'}), 400
        
        # Convert max_posts to int if provided
        if max_posts:
            try:
                max_posts = int(max_posts)
            except (ValueError, TypeError):
                max_posts = None
        
        # Parse input (username or URL)
        parsed = parse_instagram_url(input_value)
        content_type = parsed['type']
        identifier = parsed['identifier']
        
        logger.info(f"Parsed input: type={content_type}, identifier={identifier}, max_posts={max_posts}")
        
        # Create job
        job_id = str(uuid.uuid4())
        job = DownloadJob(job_id, 'single', [identifier])
        download_jobs[job_id] = job
        
        # Start download based on content type
        if content_type in ['post', 'reel', 'igtv']:
            # Single content download
            thread = threading.Thread(
                target=download_single_post_task,
                args=(job, identifier, content_type)
            )
            message = f'{content_type.capitalize()} download started'
        else:
            # Profile download
            thread = threading.Thread(
                target=download_profile_task,
                args=(job, identifier, max_posts)
            )
            message = f'Profile download started for {identifier}'
        
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


@app.route('/api/download/batch', methods=['POST'])
def download_batch():
    """Download multiple profiles API - supports URLs and usernames"""
    try:
        data = request.get_json()
        profiles = data.get('profiles', [])
        max_posts = data.get('max_posts')
        
        if not profiles or not isinstance(profiles, list):
            return jsonify({'error': 'Profiles list is required'}), 400
        
        # Clean and parse profiles (can be usernames or URLs)
        parsed_profiles = []
        for p in profiles:
            p = p.strip()
            if p:
                parsed = parse_instagram_url(p)
                if parsed['type'] == 'profile':
                    parsed_profiles.append(parsed['username'])
        
        if not parsed_profiles:
            return jsonify({'error': 'No valid profiles provided'}), 400
        
        # Convert max_posts to int
        if max_posts:
            try:
                max_posts = int(max_posts)
            except (ValueError, TypeError):
                max_posts = None
        
        logger.info(f"Batch download: {len(parsed_profiles)} profiles, max_posts={max_posts}")
        
        # Create job
        job_id = str(uuid.uuid4())
        job = DownloadJob(job_id, 'batch', parsed_profiles)
        download_jobs[job_id] = job
        
        # Start download in background
        thread = threading.Thread(
            target=download_batch_task,
            args=(job, max_posts)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': f'Batch download started for {len(parsed_profiles)} profiles'
        })
        
    except Exception as e:
        logger.error(f"Batch download error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get job status"""
    job = download_jobs.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job.to_dict())


@app.route('/api/jobs', methods=['GET'])
def get_all_jobs():
    """Get all jobs"""
    return jsonify([job.to_dict() for job in download_jobs.values()])


@app.route('/api/download/file/<path:filepath>', methods=['GET'])
def download_file(filepath):
    """Download a file"""
    try:
        # Security: ensure filepath is within downloads directory
        safe_path = Path("downloads") / filepath
        
        if not safe_path.exists():
            return jsonify({'error': 'File not found'}), 404
        
        if safe_path.is_file():
            return send_file(safe_path, as_attachment=True)
        elif safe_path.is_dir():
            # Create ZIP file
            zip_path = Path(app.config['DOWNLOAD_FOLDER']) / f"{safe_path.name}.zip"
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(safe_path):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(safe_path.parent)
                        zipf.write(file_path, arcname)
            
            return send_file(zip_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/profiles/list', methods=['GET'])
def list_profiles():
    """List all downloaded profiles"""
    try:
        downloads_dir = Path("downloads")
        
        if not downloads_dir.exists():
            return jsonify([])
        
        profiles = []
        for profile_dir in downloads_dir.iterdir():
            if profile_dir.is_dir() and not profile_dir.name.startswith('.'):
                # Count files
                photo_count = len(list((profile_dir / "photos").glob("*"))) if (profile_dir / "photos").exists() else 0
                video_count = len(list((profile_dir / "videos").glob("*"))) if (profile_dir / "videos").exists() else 0
                
                # Get metadata
                metadata_file = profile_dir / "metadata.json"
                metadata = {}
                if metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                
                profiles.append({
                    'username': profile_dir.name,
                    'photo_count': photo_count,
                    'video_count': video_count,
                    'path': str(profile_dir),
                    'metadata': metadata
                })
        
        return jsonify(profiles)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get download statistics"""
    try:
        stats = {
            'total_jobs': len(download_jobs),
            'completed_jobs': sum(1 for job in download_jobs.values() if job.status == 'completed'),
            'failed_jobs': sum(1 for job in download_jobs.values() if job.status == 'failed'),
            'running_jobs': sum(1 for job in download_jobs.values() if job.status == 'running'),
            'total_profiles': sum(len(job.profiles) for job in download_jobs.values()),
            'successful_downloads': sum(len(job.completed_profiles) for job in download_jobs.values()),
            'failed_downloads': sum(len(job.failed_profiles) for job in download_jobs.values())
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/limits', methods=['GET'])
def get_limits():
    """Get rate limits and usage information"""
    return jsonify({
        'rate_limits': {
            'posts_per_profile': {
                'recommended': 50,
                'maximum': 200,
                'description': 'Instagram may throttle after 200 posts per session'
            },
            'profiles_per_batch': {
                'recommended': 5,
                'maximum': 10,
                'description': 'Batch downloads should be limited to avoid detection'
            },
            'requests_per_hour': {
                'safe': 200,
                'limit': 500,
                'description': 'Instagram allows ~200-500 requests per hour'
            },
            'delay_between_profiles': {
                'minimum': 3,
                'recommended': 5,
                'unit': 'seconds',
                'description': 'Wait time between batch profile downloads'
            }
        },
        'usage_guidelines': {
            'session_limits': 'Use session files to maintain login state',
            'best_practices': [
                'Download public profiles only',
                'Use reasonable post limits (50-100)',
                'Add delays between batch downloads',
                'Avoid excessive requests in short periods',
                'Respect Instagram Terms of Service'
            ],
            'legal_notice': 'This tool is for personal, educational use only. Users are responsible for compliance with Instagram Terms of Service and applicable laws.'
        },
        'technical_info': {
            'max_file_size': '100MB per download',
            'supported_content': ['photos', 'videos', 'carousels', 'reels'],
            'unsupported': ['private profiles', 'stories (requires login)', 'highlights (requires login)']
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Instagram Downloader - Web Interface")
    print("="*60)
    print("\nInitializing...")
    
    if initialize_downloader():
        print("✅ Downloader initialized successfully")
        print("\nStarting web server...")
        print("🌐 Open browser: http://localhost:5000")
        print("\nPress Ctrl+C to stop")
        print("="*60 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    else:
        print("❌ Failed to initialize downloader")
        sys.exit(1)
