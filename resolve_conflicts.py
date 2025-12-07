#!/usr/bin/env python3
"""
Resolve Git merge conflicts in XML files
Keeps the HEAD version (current branch) and removes conflict markers
"""

import os
import re
from pathlib import Path

def resolve_conflict(content):
    """
    Remove Git conflict markers and keep HEAD version
    
    Handles multiple patterns:
    1. <<<<<<< HEAD ... ======= ... >>>>>>> branch
    2. Standalone markers that weren't cleaned up
    """
    # First pass: Remove complete conflict blocks, keep HEAD content
    conflict_pattern = r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> .*?\n'
    resolved = re.sub(
        conflict_pattern,
        r'\1\n',
        content,
        flags=re.DOTALL
    )
    
    # Second pass: Remove any remaining standalone markers
    resolved = re.sub(r'<<<<<<< HEAD\n?', '', resolved)
    resolved = re.sub(r'=======\n?', '', resolved)
    resolved = re.sub(r'>>>>>>> .*?\n?', '', resolved)
    
    return resolved

def main():
    nga4_dir = Path('/home/thaianh/Study/GreenWave/src/backend/app/sumo_rl/sumo_files/Nga4ThuDuc')
    
    print("🔍 Resolving Git merge conflicts in Nga4ThuDuc files...\n")
    
    fixed_count = 0
    
    # Process all XML and sumocfg files
    for pattern in ['*.xml', '*.sumocfg']:
        for filepath in nga4_dir.glob(pattern):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file has conflicts
            if '<<<<<<< HEAD' in content:
                print(f"🔧 Resolving {filepath.name}...")
                
                # Resolve conflicts
                resolved_content = resolve_conflict(content)
                
                # Write back
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(resolved_content)
                
                fixed_count += 1
                print(f"   ✅ Fixed")
            else:
                print(f"   ✓ {filepath.name} - No conflicts")
    
    print(f"\n✅ Resolved conflicts in {fixed_count} files")

if __name__ == '__main__':
    main()
