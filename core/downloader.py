#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Downloader - Core Download Functions
Enhanced downloader with support for profile pics, stories, posts, reels, IGTV
"""

import os
import sys
import logging
import time
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union
from instaloader import Instaloader, Profile, Post, StoryItem
import instaloader

logger = logging.getLogger(__name__)


class InstagramDownloader:
    """Enhanced Instagram downloader with comprehensive features"""
    
    def __init__(self, loader: Instaloader):
        self.loader = loader
        
    def download_profile_picture(self, username: str, download_dir: Path) -> Dict:
        """Download profile picture in HD quality"""
        try:
            profile = Profile.from_username(self.loader.context, username)
            
            # Create directory
            pic_dir = download_dir / "profile_picture"
            pic_dir.mkdir(parents=True, exist_ok=True)
            
            # Download HD profile pic
            pic_url = profile.profile_pic_url
            pic_filename = pic_dir / f"{username}_profile_pic.jpg"
            
            logger.info(f"Downloading profile picture for {username}")
            response = requests.get(pic_url, stream=True)
            response.raise_for_status()
            
            with open(pic_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return {
                'success': True,
                'file': str(pic_filename),
                'url': pic_url,
                'size': pic_filename.stat().st_size
            }
            
        except Exception as e:
            logger.error(f"Failed to download profile picture for {username}: {e}")
            return {'success': False, 'error': str(e)}
    
    def download_stories(self, username: str, download_dir: Path) -> Dict:
        """Download all available stories for a user"""
        try:
            profile = Profile.from_username(self.loader.context, username)
            
            # Create directory
            stories_dir = download_dir / "stories"
            stories_dir.mkdir(parents=True, exist_ok=True)
            
            # Get stories
            stories = []
            downloaded_count = 0
            failed_count = 0
            
            logger.info(f"Fetching stories for {username}")
            
            try:
                for story in self.loader.get_stories(userids=[profile.userid]):
                    for item in story.get_items():
                        try:
                            # Download story item
                            self.loader.download_storyitem(item, stories_dir)
                            downloaded_count += 1
                            stories.append({
                                'date': item.date_local.isoformat(),
                                'type': 'video' if item.is_video else 'photo'
                            })
                        except Exception as e:
                            logger.error(f"Failed to download story item: {e}")
                            failed_count += 1
            except Exception as e:
                # Stories might not be available (requires login or no stories)
                logger.warning(f"Could not fetch stories for {username}: {e}")
                return {
                    'success': False,
                    'error': 'Stories not available (requires login or no active stories)',
                    'downloaded': 0,
                    'failed': 0
                }
            
            return {
                'success': downloaded_count > 0,
                'downloaded': downloaded_count,
                'failed': failed_count,
                'stories': stories
            }
            
        except Exception as e:
            logger.error(f"Failed to download stories for {username}: {e}")
            return {'success': False, 'error': str(e), 'downloaded': 0, 'failed': 0}
    
    def download_highlights(self, username: str, download_dir: Path) -> Dict:
        """Download all highlights for a user"""
        try:
            profile = Profile.from_username(self.loader.context, username)
            
            # Create directory
            highlights_dir = download_dir / "highlights"
            highlights_dir.mkdir(parents=True, exist_ok=True)
            
            downloaded_count = 0
            failed_count = 0
            highlights_list = []
            
            logger.info(f"Fetching highlights for {username}")
            
            try:
                for highlight in self.loader.get_highlights(profile):
                    highlight_name = highlight.title
                    highlight_dir = highlights_dir / highlight_name
                    highlight_dir.mkdir(parents=True, exist_ok=True)
                    
                    for item in highlight.get_items():
                        try:
                            self.loader.download_storyitem(item, highlight_dir)
                            downloaded_count += 1
                        except Exception as e:
                            logger.error(f"Failed to download highlight item: {e}")
                            failed_count += 1
                    
                    highlights_list.append({
                        'title': highlight_name,
                        'items': downloaded_count
                    })
            except Exception as e:
                logger.warning(f"Could not fetch highlights for {username}: {e}")
                return {
                    'success': False,
                    'error': 'Highlights not available (requires login)',
                    'downloaded': 0,
                    'failed': 0
                }
            
            return {
                'success': downloaded_count > 0,
                'downloaded': downloaded_count,
                'failed': failed_count,
                'highlights': highlights_list
            }
            
        except Exception as e:
            logger.error(f"Failed to download highlights for {username}: {e}")
            return {'success': False, 'error': str(e), 'downloaded': 0, 'failed': 0}
    
    def download_posts(self, username: str, download_dir: Path, max_posts: int = None) -> Dict:
        """Download posts with proper counting"""
        try:
            profile = Profile.from_username(self.loader.context, username)
            
            # Create directories
            posts_dir = download_dir / "posts"
            posts_dir.mkdir(parents=True, exist_ok=True)
            
            # Determine how many posts to download
            total_available = profile.mediacount
            total_to_download = min(total_available, max_posts) if max_posts else total_available
            
            downloaded_count = 0
            failed_count = 0
            posts_info = []
            
            logger.info(f"Downloading posts for {username}: {total_to_download} of {total_available}")
            
            for post in profile.get_posts():
                if max_posts and downloaded_count >= max_posts:
                    break
                
                try:
                    # Download post
                    self.loader.download_post(post, target=str(posts_dir))
                    downloaded_count += 1
                    
                    posts_info.append({
                        'shortcode': post.shortcode,
                        'date': post.date_local.isoformat(),
                        'likes': post.likes,
                        'comments': post.comments,
                        'is_video': post.is_video,
                        'caption': post.caption[:100] if post.caption else ''
                    })
                    
                    # Small delay
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Failed to download post {post.shortcode}: {e}")
                    failed_count += 1
            
            return {
                'success': True,
                'total_available': total_available,
                'total_downloaded': downloaded_count,
                'failed': failed_count,
                'posts': posts_info
            }
            
        except Exception as e:
            logger.error(f"Failed to download posts for {username}: {e}")
            return {'success': False, 'error': str(e), 'total_downloaded': 0, 'failed': 0}
    
    def download_single_post(self, shortcode: str, download_dir: Path) -> Dict:
        """Download a single post by shortcode"""
        try:
            post = Post.from_shortcode(self.loader.context, shortcode)
            username = post.owner_username
            
            # Create directory
            post_dir = download_dir / f"{username}_post_{shortcode}"
            post_dir.mkdir(parents=True, exist_ok=True)
            
            # Download
            self.loader.download_post(post, target=str(post_dir))
            
            return {
                'success': True,
                'username': username,
                'shortcode': shortcode,
                'is_video': post.is_video,
                'likes': post.likes,
                'comments': post.comments,
                'path': str(post_dir)
            }
            
        except Exception as e:
            logger.error(f"Failed to download post {shortcode}: {e}")
            return {'success': False, 'error': str(e)}
    
    def count_downloaded_media(self, download_dir: Path) -> Dict:
        """Count all downloaded media files in a directory"""
        counts = {
            'photos': 0,
            'videos': 0,
            'total': 0
        }
        
        if not download_dir.exists():
            return counts
        
        # Count files by extension
        for file in download_dir.rglob('*'):
            if file.is_file():
                ext = file.suffix.lower()
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    counts['photos'] += 1
                    counts['total'] += 1
                elif ext in ['.mp4', '.mov', '.avi', '.webm']:
                    counts['videos'] += 1
                    counts['total'] += 1
        
        return counts
