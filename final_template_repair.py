import os
import re

templates_dir = r'd:\project\inventory_systems\inventory_systems\templates'

def repair_template(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        except:
            return False

    original_content = content

    # 1. Join split tags {% ... %}
    def clean_tag(match):
        inner = match.group(1)
        inner = re.sub(r'\s+', ' ', inner).strip()
        return f'{{% {inner} %}}'

    content = re.compile(r'\{%(.*?)%\}', re.DOTALL).sub(clean_tag, content)

    # 2. Join split variables {{ ... }}
    def clean_var(match):
        inner = match.group(1)
        inner = re.sub(r'\s+', ' ', inner).strip()
        return f'{{{{ {inner} }}}}'

    content = re.compile(r'\{\{(.*?)\}\}', re.DOTALL).sub(clean_var, content)

    # 3. Handle split operators like < = or = =
    def join_split_ops(match):
        prefix = match.group(1)
        expr = match.group(2)
        
        # Specific patterns for split operators
        expr = re.sub(r'<\s*=', '<=', expr)
        expr = re.sub(r'>\s*=', '>=', expr)
        expr = re.sub(r'!\s*=', '!=', expr)
        expr = re.sub(r'=\s*=', '==', expr)
        
        return f'{{% {prefix} {expr} %}}'

    content = re.sub(r'\{%\s*(if|elif)\s+(.*?)\s*%\}', join_split_ops, content)

    # 4. Fix missing spaces around operators
    operators = ['==', '!=', '<=', '>=', '<', '>']
    
    def fix_operator_spacing(match):
        prefix = match.group(1)
        expr = match.group(2)
        
        for op in operators:
            # Add spaces around operator
            expr = re.sub(rf'\s*{re.escape(op)}\s*', f' {op} ', expr)
            
        expr = re.sub(r'\s+', ' ', expr).strip()
        return f'{{% {prefix} {expr} %}}'

    content = re.sub(r'\{%\s*(if|elif)\s+(.*?)\s*%\}', fix_operator_spacing, content)

    # 5. Global cleanup
    content = content.replace('{% else %}', '{% else %}')
    content = content.replace('{% endif %}', '{% endif %}')
    content = content.replace('{% empty %}', '{% empty %}')
    content = content.replace('{% endfor %}', '{% endfor %}')

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        return True
    return False

print("Starting global template repair...")
fixed_count = 0
for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            try:
                if repair_template(os.path.join(root, file)):
                    print(f"Repaired: {os.path.relpath(os.path.join(root, file), templates_dir)}")
                    fixed_count += 1
            except Exception as e:
                print(f"Error repairing {file}: {e}")

print(f"Finished! Total templates repaired: {fixed_count}")
