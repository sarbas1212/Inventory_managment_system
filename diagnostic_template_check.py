import os
import django
from django.conf import settings
from django.template import Template, Context, TemplateSyntaxError

# Configure minimal Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [r'd:\project\inventory_systems\inventory_systems\templates'],
        }]
    )
    django.setup()

templates_dir = r'd:\project\inventory_systems\inventory_systems\templates'

def check_templates():
    print("Starting Template Diagnostics...")
    errors_found = 0
    files_checked = 0
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                files_checked += 1
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Try to parse the template
                    Template(content)
                except TemplateSyntaxError as e:
                    print(f"\n[!] ERROR in {os.path.relpath(path, templates_dir)}:")
                    print(f"    {e}")
                    errors_found += 1
                except Exception as e:
                    print(f"\n[?] Unexpected Error in {file}: {e}")
                    
    print(f"\nDiagnostics Finished.")
    print(f"Checked: {files_checked} files.")
    print(f"Errors found: {errors_found}")
    return errors_found

if __name__ == "__main__":
    check_templates()
