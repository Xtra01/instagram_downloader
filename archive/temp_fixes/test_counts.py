#!/usr/bin/env python3
"""
Test file counts to debug the issue
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.downloader import InstagramDownloader

def test_file_counts():
    """Test count_downloaded_media with real paths"""
    print("=" * 70)
    print("FILE COUNT DEBUG TEST")
    print("=" * 70)
    
    # Create downloader with loader
    import instaloader
    loader = instaloader.Instaloader()
    downloader = InstagramDownloader(loader)
    
    # Test different paths
    test_paths = [
        Path("d:/CodeProjects/instagram_downloader/downloads/sernaelisafit"),
        Path("downloads/sernaelisafit"),
        Path("./downloads/sernaelisafit"),
    ]
    
    for test_path in test_paths:
        print(f"\n{'='*70}")
        print(f"Testing path: {test_path}")
        print(f"Absolute: {test_path.absolute()}")
        print(f"Exists: {test_path.exists()}")
        
        if test_path.exists():
            # Count manually first
            print(f"\nManual file listing:")
            
            photo_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
            video_exts = {'.mp4', '.mov', '.avi', '.webm', '.mkv'}
            
            manual_photos = 0
            manual_videos = 0
            
            for file in test_path.rglob('*'):
                if file.is_file() and not file.name.startswith('.'):
                    ext = file.suffix.lower()
                    if ext in photo_exts:
                        manual_photos += 1
                        print(f"  PHOTO: {file.relative_to(test_path)}")
                    elif ext in video_exts:
                        manual_videos += 1
                        print(f"  VIDEO: {file.relative_to(test_path)}")
            
            print(f"\nManual count: {manual_photos} photos, {manual_videos} videos")
            
            # Now test the function
            counts = downloader.count_downloaded_media(test_path)
            print(f"Function count: {counts['photos']} photos, {counts['videos']} videos")
            
            if counts['photos'] != manual_photos or counts['videos'] != manual_videos:
                print("*** MISMATCH DETECTED! ***")
            else:
                print("OK - Counts match!")
        else:
            print("*** Path does not exist! ***")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_file_counts()
