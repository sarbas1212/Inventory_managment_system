import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_systems.settings')
try:
    django.setup()
    print("Django setup successful")
    from django.apps import apps
    for app in apps.get_app_configs():
        try:
            app.import_models()
            print(f"Loaded models for {app.label}")
        except Exception as e:
            print(f"Failed to load models for {app.label}: {e}")
except Exception as e:
    print(f"Django setup failed: {e}")
    import traceback
    traceback.print_exc()
