import os
import re

templates_dir = r'd:\project\inventory_systems\inventory_systems\templates'

split_tags = []

for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Find all {% ... %} including multi-line
                all_blocks = re.findall(r'\{%.*?%\}', content, re.DOTALL)
                for block in all_blocks:
                    if '\n' in block:
                        split_tags.append((filepath, block))
                
                all_vars = re.findall(r'\{\{.*?\}\}', content, re.DOTALL)
                for var in all_vars:
                    if '\n' in var:
                        split_tags.append((filepath, var))

if split_tags:
    print(f"Found {len(split_tags)} split tags:")
    for filepath, tag in split_tags:
        rel_path = os.path.relpath(filepath, templates_dir)
        print(f"File: {rel_path}")
        print(f"Tag: {tag!r}")
        print("-" * 20)
else:
    print("No split tags found.")
