import os
import re

templates_dir = r'd:\project\inventory_systems\inventory_systems\templates'
operators = ['==', '!=', '<=', '>=', '<', '>']

def fix_operator_spacing(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Pattern to find {% if ... %} and {% elif ... %}
    def repair_tag(match):
        prefix = match.group(1) # if or elif
        expr = match.group(2)
        
        # Protect strings to avoid replacing inside them (simple approach)
        # However, operators inside strings in Django templates are rare or quoted
        
        for op in operators:
            # Replace op with spaced version, but avoid double spacing
            # Use negative lookahead/lookbehind to ensure we don't matches already spaced ones
            # Or just replace all occurrences and then collapse double spaces
            expr = re.sub(rf'\s*{re.escape(op)}\s*', f' {op} ', expr)
            
        # Collapse multi-spaces
        expr = re.sub(r'\s+', ' ', expr).strip()
        return f'{{% {prefix} {expr} %}}'

    content = re.sub(r'\{%\s*(if|elif)\s+(.*?)\s*%\}', repair_tag, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        return True
    return False

print("Starting global operator spacing repair...")
count = 0
for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            if fix_operator_spacing(os.path.join(root, file)):
                print(f"Fixed spacing: {file}")
                count += 1
print(f"Done. Repaired {count} files.")
