#!/usr/bin/env python3
"""
FINAL FIX - Move all files from Unicode paths to correct locations
"""
import os
import shutil
from pathlib import Path
import glob

def find_and_fix_all_unicode_paths():
    """Find ALL directories with Unicode issues and fix them"""
    base_dir = Path(__file__).parent
    downloads_dir = base_dir / "downloads"
    
    print("=" * 70)
    print("FINAL PATH FIX - Finding ALL Unicode issues")
    print("=" * 70)
    
    fixed_count = 0
    total_files_moved = 0
    
    # Use os.walk to find ALL directories
    for root, dirs, files in os.walk(str(base_dir)):
        root_path = Path(root)
        
        # Check if this path has Unicode characters
        has_unicode = any(ord(c) > 127 for c in root)
        
        if has_unicode and files:
            print(f"\nFound Unicode path with {len(files)} files:")
            print(f"  Source: {root[:80]}...")
            
            # Try to determine the correct target path
            # Extract the meaningful parts after "downloads"
            root_str = str(root)
            
            # Handle the weird "d：﹨CodeProjects﹨..." format
            if "CodeProjects" in root_str and "downloads" in root_str:
                # Find the part after "downloads"
                try:
                    # Split and find downloads
                    parts = root_str.split("downloads")
                    if len(parts) >= 2:
                        after_downloads = parts[-1]
                        # Clean up Unicode characters
                        after_downloads = after_downloads.replace('﹨', os.sep)
                        after_downloads = after_downloads.replace('：', ':')
                        after_downloads = after_downloads.lstrip(os.sep)
                        
                        # Build target path
                        target_path = downloads_dir / after_downloads
                        
                        print(f"  Target: {target_path}")
                        
                        # Create target directory
                        target_path.mkdir(parents=True, exist_ok=True)
                        
                        # Copy files
                        files_copied = 0
                        for file in files:
                            src_file = root_path / file
                            dest_file = target_path / file
                            
                            try:
                                if not dest_file.exists():
                                    shutil.copy2(src_file, dest_file)
                                    files_copied += 1
                                    print(f"    -> {file}")
                            except Exception as e:
                                print(f"    ERROR copying {file}: {e}")
                        
                        print(f"  Copied {files_copied} files")
                        total_files_moved += files_copied
                        fixed_count += 1
                        
                except Exception as e:
                    print(f"  ERROR processing path: {e}")
    
    # Now remove the Unicode directories
    print(f"\n{'='*70}")
    print("Cleaning up Unicode directories...")
    
    for item in base_dir.iterdir():
        if item.is_dir():
            has_unicode = any(ord(c) > 127 for c in item.name)
            if has_unicode:
                try:
                    shutil.rmtree(item)
                    print(f"  Removed: {item.name[:60]}...")
                except Exception as e:
                    print(f"  Could not remove {item.name[:60]}: {e}")
    
    print(f"\n{'='*70}")
    print(f"COMPLETE!")
    print(f"  Fixed {fixed_count} Unicode paths")
    print(f"  Moved {total_files_moved} files")
    print("=" * 70)

if __name__ == "__main__":
    find_and_fix_all_unicode_paths()
