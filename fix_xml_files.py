#!/usr/bin/env python3
"""Fix XML files to have XML declaration at the beginning"""

import os
import re
from pathlib import Path

def fix_xml_file(filepath):
    """Fix a single XML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file starts with XML declaration
    if content.strip().startswith('<?xml'):
        print(f"✓ {filepath.name} - Already correct")
        return False
    
    # Find the XML declaration
    xml_decl_pattern = r'<\?xml[^?]*\?>'
    match = re.search(xml_decl_pattern, content)
    
    if not match:
        print(f"✗ {filepath.name} - No XML declaration found")
        return False
    
    # Extract XML declaration
    xml_decl = match.group(0)
    
    # Remove the XML declaration from its current position
    content_without_decl = content.replace(xml_decl, '', 1)
    
    # Remove leading whitespace/newlines but keep copyright comments
    content_without_decl = content_without_decl.lstrip('\n')
    
    # Put XML declaration at the beginning
    new_content = xml_decl + '\n' + content_without_decl
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ {filepath.name} - Fixed")
    return True

def main():
    # Path to Nga4ThuDuc directory
    nga4_dir = Path('/home/thaianh/Study/GreenWave/src/backend/app/sumo_rl/sumo_files/Nga4ThuDuc')
    
    print("Fixing XML files in Nga4ThuDuc directory...\n")
    
    fixed_count = 0
    
    # Fix all .xml and .sumocfg files
    for pattern in ['*.xml', '*.sumocfg']:
        for filepath in nga4_dir.glob(pattern):
            if fix_xml_file(filepath):
                fixed_count += 1
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == '__main__':
    main()
