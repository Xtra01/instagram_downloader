#!/usr/bin/env python3
"""
Fix Unicode path issues - Move files from old Unicode paths to normal paths
"""
import os
import shutil
from pathlib import Path

def fix_unicode_paths():
    """Move files from Unicode paths to normal paths"""
    base_dir = Path(__file__).parent
    
    # Find all directories with Unicode characters (including U+FE68)
    unicode_chars = ['﹨', '：']  # Unicode backslash and colon
    
    fixed_count = 0
    for item in base_dir.iterdir():
        if not item.is_dir():
            continue
            
        # Check if name contains Unicode characters
        has_unicode = any(ord(c) > 127 for c in item.name)
        
        if has_unicode:
            print(f"\nFound Unicode path: {item.name[:60]}...")
            
            # Replace Unicode characters with normal equivalents
            normal_name = item.name
            normal_name = normal_name.replace('﹨', os.sep)  # U+FE68 → \
            normal_name = normal_name.replace('：', ':')     # U+FF1A → :
            
            # Skip if already in correct downloads folder
            if normal_name.startswith('downloads' + os.sep):
                # Extract the part after "downloads\"
                parts = normal_name.split(os.sep)
                if len(parts) > 1:
                    # Use relative path under downloads/
                    normal_path = base_dir / 'downloads' / os.sep.join(parts[1:])
                else:
                    normal_path = base_dir / normal_name
            else:
                normal_path = base_dir / normal_name
            
            print(f"  → Target: {normal_path}")
            
            try:
                # Create parent directories
                normal_path.parent.mkdir(parents=True, exist_ok=True)
                
                if normal_path.exists():
                    # Merge: copy files from source to destination
                    print(f"  → Merging with existing directory...")
                    copied = 0
                    
                    for root, dirs, files in os.walk(item):
                        for file in files:
                            src_file = Path(root) / file
                            
                            # Calculate relative path from source root
                            try:
                                rel_path = src_file.relative_to(item)
                            except ValueError:
                                continue
                            
                            dest_file = normal_path / rel_path
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            
                            if not dest_file.exists():
                                shutil.copy2(src_file, dest_file)
                                copied += 1
                                print(f"    ✓ {file}")
                    
                    print(f"  → Copied {copied} files")
                    
                    # Remove old directory after successful copy
                    try:
                        shutil.rmtree(item)
                        print(f"  ✓ Removed old directory")
                        fixed_count += 1
                    except Exception as e:
                        print(f"  ⚠ Could not remove old directory: {e}")
                else:
                    # Simple move
                    shutil.move(str(item), str(normal_path))
                    print(f"  ✓ Moved successfully")
                    fixed_count += 1
                    
            except Exception as e:
                print(f"  ✗ Error: {e}")
                import traceback
                traceback.print_exc()
    
    return fixed_count

if __name__ == "__main__":
    print("=" * 60)
    print("Instagram Downloader - Path Fixer")
    print("=" * 60)
    print("\nSearching for Unicode path issues...")
    
    fixed = fix_unicode_paths()
    
    print("\n" + "=" * 60)
    if fixed > 0:
        print(f"✓ Fixed {fixed} directories with Unicode paths!")
    else:
        print("ℹ No Unicode path issues found.")
    print("=" * 60)
