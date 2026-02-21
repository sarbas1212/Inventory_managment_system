import os
import re

templates_dir = r'd:\project\inventory_systems\inventory_systems\templates'

def force_join_tags(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # regex to find {% ... %} accurately including nesting (not really needed for Django, but re.DOTALL is enough)
    # We use a non-greedy match that looks for the closest closing %}
    content = re.sub(r'\{%(.*?)%\}', lambda m: '{% ' + re.sub(r'\s+', ' ', m.group(1)).strip() + ' %}', content, flags=re.DOTALL)
    content = re.sub(r'\{\{(.*?)\}\}', lambda m: '{{ ' + re.sub(r'\s+', ' ', m.group(1)).strip() + ' }}', content, flags=re.DOTALL)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        return True
    return False

print("Starting forced join...")
count = 0
for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            if force_join_tags(os.path.join(root, file)):
                print(f"Fixed: {file}")
                count += 1
print(f"Done. Fixed {count} files.")
