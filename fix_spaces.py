import os
import re

templates_dir = r'd:\project\inventory_systems\inventory_systems\templates'

operators = ['==', '!=', '<=', '>=', '<', '>']

def fix_spaces_in_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Target {% if ... %} and {% elif ... %}
    pattern = re.compile(r'\{%\s*(if|elif)\s+(.*?)\s*%\}', re.DOTALL)
    
    def replace_op(match):
        tag_type = match.group(1)
        expression = match.group(2)
        
        # Add spaces around operators if missing
        for op in operators:
            # Match operator not preceded by space or not followed by space
            # but careful with >= and <= not being partially matched with < or > (though we only check these 4)
            # The pattern below ensures the operator has at least one space on each side
            # We use a loop to handle multiple occurrences
            old_expr = ""
            while old_expr != expression:
                old_expr = expression
                # Case 1: something==something -> something == something
                # Case 2: something ==something -> something == something
                # Case 3: something== something -> something == something
                
                # We need to be careful not to keep adding spaces if they already exist
                expression = re.sub(rf'([^ ])({re.escape(op)})', r'\1 \2', expression)
                expression = re.sub(rf'({re.escape(op)})([^ ])', r'\1 \2', expression)
        
        # Cleanup double spaces just in case
        expression = re.sub(r' +', ' ', expression).strip()
        
        return f'{{% {tag_type} {expression} %}}'

    new_content = pattern.sub(replace_op, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)
        print(f"Fixed spaces in {filepath}")
    else:
        print(f"No changes needed for {filepath}")

for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            fix_spaces_in_tags(os.path.join(root, file))
