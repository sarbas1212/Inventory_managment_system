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

    # Join split operators globally within tags
    def join_ops_in_tag(match):
        tag = match.group(0)
        tag = re.sub(r'<\s*=', '<=', tag)
        tag = re.sub(r'>\s*=', '>=', tag)
        tag = re.sub(r'!\s*=', '!=', tag)
        tag = re.sub(r'=\s*=', '==', tag)
        return tag

    content = re.compile(r'\{%(.*?)%\}', re.DOTALL).sub(join_ops_in_tag, content)

    # Ensure spaces around operators
    operators = ['==', '!=', '<=', '>=', '<', '>']
    def space_ops_in_tag(match):
        tag_type = match.group(1) # if or elif
        expr = match.group(2)
        for op in operators:
            expr = re.sub(rf'\s*{re.escape(op)}\s*', f' {op} ', expr)
        expr = re.sub(r'\s+', ' ', expr).strip()
        return f'{{% {tag_type} {expr} %}}'

    content = re.sub(r'\{%\s*(if|elif)\s+(.*?)\s*%\}', space_ops_in_tag, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        return True
    return False

print("Starting operator repair...")
fixed_count = 0
for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            if repair_template(os.path.join(root, file)):
                print(f"Repaired: {os.path.relpath(os.path.join(root, file), templates_dir)}")
                fixed_count += 1

print(f"Finished! Total templates repaired: {fixed_count}")
