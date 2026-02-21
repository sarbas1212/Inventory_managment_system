import os
import re

templates_dir = r'd:\project\inventory_systems\inventory_systems\templates'

def comprehensive_repair(content):
    # 0. Join split tags (critical for parsing logic)
    # Match {% ... %} and {{ ... }} across lines
    def join_tags(match):
        return re.sub(r'\s+', ' ', match.group(0))
    
    content = re.sub(r'\{%.*?%\}', join_tags, content, flags=re.DOTALL)
    content = re.sub(r'\{\{.*?\}\}', join_tags, content, flags=re.DOTALL)

    # 1. Clean up split operators (e.g., < =, ! =, = =)
    content = re.sub(r'<\s*=', '<=', content)
    content = re.sub(r'>\s*=', '>=', content)
    content = re.sub(r'!\s*=', '!=', content)
    content = re.sub(r'=\s*=', '==', content)

    # 2. Repair spacing in {% if %} and {% elif %} tags robustly
    def repair_tags(match):
        prefix = match.group(1)
        tag_content = match.group(2)
        
        ops = ['==', '!=', '<=', '>=', '<', '>']
        ops_pattern = '|'.join(re.escape(op) for op in ops)
        
        parts = re.split(f'({ops_pattern})', tag_content)
        
        reconstructed = []
        for part in parts:
            if part in ops:
                reconstructed.append(f' {part} ')
            else:
                reconstructed.append(part)
        
        reconstructed_str = "".join(reconstructed)
        reconstructed_str = re.sub(r'\s+', ' ', reconstructed_str).strip()
        
        return f'{{% {prefix} {reconstructed_str} %}}'

    content = re.sub(r'\{%\s*(if|elif)\s+(.*?)\s*%\}', repair_tags, content)

    # 3. Handle {% else %} inside {% for %} -> {% empty %}
    lines = content.splitlines(keepends=True)
    new_lines = []
    tag_stack = []
    
    tag_pattern = re.compile(r'\{%\s*(for|if|else|empty|endif|endfor)\b')
    
    for line in lines:
        matches = list(tag_pattern.finditer(line))
        
        modified_line = line
        # Offset tracking for multiple replacements in one line
        offset = 0
        
        for match in matches:
            tag_name = match.group(1)
            if tag_name in ['if', 'for']:
                tag_stack.append(tag_name)
            elif tag_name in ['endif', 'endfor']:
                if tag_stack:
                    tag_stack.pop()
            elif tag_name == 'else':
                if tag_stack and tag_stack[-1] == 'for':
                    start, end = match.span()
                    # Adjust for offset from previous replacements
                    adj_start = start + offset
                    adj_end = end + offset
                    
                    replacement = '{% empty %}'
                    modified_line = modified_line[:adj_start] + replacement + modified_line[adj_end:]
                    offset += len(replacement) - (end - start)
            
        new_lines.append(modified_line)
            
    content = "".join(new_lines)
    return content

def run_repair():
    print("Starting Comprehensive Template Repair (v3)...")
    files_processed = 0
    files_modified = 0
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                files_processed += 1
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        original_content = f.read()
                    
                    repaired_content = comprehensive_repair(original_content)
                    
                    if repaired_content != original_content:
                        with open(path, 'w', encoding='utf-8', newline='\n') as f:
                            f.write(repaired_content)
                        print(f"Repaired: {file}")
                        files_modified += 1
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                    
    print(f"Done. Processed {files_processed} files, modified {files_modified}.")

if __name__ == "__main__":
    run_repair()
