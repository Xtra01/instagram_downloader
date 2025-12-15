#!/usr/bin/env python3
"""
Integration test - Full system test
"""
import sys
import requests
from pathlib import Path

def test_full_system():
    """Test the entire system"""
    print("=" * 70)
    print("INTEGRATION TEST - Full System")
    print("=" * 70)
    
    base_url = "http://localhost:5000"
    
    # Test 1: List profiles endpoint
    print("\n[1/3] Testing /api/profiles/list endpoint...")
    try:
        response = requests.get(f"{base_url}/api/profiles/list", timeout=5)
        if response.status_code == 200:
            profiles = response.json()
            print(f"  ✓ Got {len(profiles)} profiles")
            
            # Find sernaelisafit
            serna = next((p for p in profiles if p['username'] == 'sernaelisafit'), None)
            if serna:
                print(f"  ✓ sernaelisafit found:")
                print(f"    - Photos: {serna['photo_count']}")
                print(f"    - Videos: {serna['video_count']}")
                print(f"    - Total: {serna['total_count']}")
                
                if serna['photo_count'] == 47 and serna['video_count'] == 4:
                    print("  ✓✓ CORRECT COUNTS!")
                else:
                    print(f"  ✗ WRONG COUNTS! Expected 47 photos, 4 videos")
                    return False
            else:
                print("  ✗ sernaelisafit not found!")
                return False
        else:
            print(f"  ✗ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Test 2: Check files on disk
    print("\n[2/3] Testing file counts on disk...")
    try:
        downloads_dir = Path("d:/CodeProjects/instagram_downloader/downloads/sernaelisafit")
        
        photo_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        video_exts = {'.mp4', '.mov', '.avi', '.webm', '.mkv'}
        
        photos = sum(1 for f in downloads_dir.rglob('*') if f.is_file() and f.suffix.lower() in photo_exts and not f.name.startswith('.'))
        videos = sum(1 for f in downloads_dir.rglob('*') if f.is_file() and f.suffix.lower() in video_exts and not f.name.startswith('.'))
        
        print(f"  Disk count: {photos} photos, {videos} videos")
        
        if photos == 47 and videos == 4:
            print("  ✓ Disk counts match API!")
        else:
            print(f"  ✗ Disk counts don't match! Expected 47 photos, 4 videos")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Test 3: Check for Unicode path issues
    print("\n[3/3] Checking for Unicode path issues...")
    try:
        base_dir = Path("d:/CodeProjects/instagram_downloader")
        
        unicode_paths = []
        for item in base_dir.iterdir():
            if item.is_dir():
                has_unicode = any(ord(c) > 127 for c in item.name)
                if has_unicode:
                    unicode_paths.append(item.name)
        
        if unicode_paths:
            print(f"  ✗ Found {len(unicode_paths)} Unicode paths:")
            for p in unicode_paths[:3]:
                print(f"    - {p[:60]}...")
            return False
        else:
            print("  ✓ No Unicode path issues!")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("ALL TESTS PASSED!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_full_system()
    sys.exit(0 if success else 1)
