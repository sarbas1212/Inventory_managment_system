from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Setup initial roles and permissions'

    def handle(self, *args, **options):
        roles = {
            'Admin': '__all__',
            'Accountant': {
                'apps': ['accounts_ledger', 'invoices', 'purchases', 'payments', 'vendors'],
                'models': {
                    'customers': ['view'],
                    'inventory': ['view'],
                }
            },
            'Store Manager': {
                'apps': ['inventory', 'products'],
                'models': {
                    'purchases': ['view'],
                    'invoices': ['view'],
                }
            },
            'Sales Staff': {
                'models': {
                    'invoices': ['add', 'change', 'view'],
                    'customers': ['add', 'change', 'view'],
                    'products': ['view'],
                }
            }
        }

        for role_name, perms_config in roles.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(f"Created group: {role_name}")
            else:
                self.stdout.write(f"Updated group: {role_name}")

            # Clear existing permissions to reset
            group.permissions.clear()

            if perms_config == '__all__':
                # Admin gets all permissions
                all_perms = Permission.objects.all()
                group.permissions.set(all_perms)
                continue

            permissions_to_add = []

            # 1. App-level full access
            if 'apps' in perms_config:
                for app_label in perms_config['apps']:
                    content_types = ContentType.objects.filter(app_label=app_label)
                    perms = Permission.objects.filter(content_type__in=content_types)
                    permissions_to_add.extend(perms)

            # 2. Specific model access
            if 'models' in perms_config:
                for app_model, actions in perms_config['models'].items():
                    # Handle app_label vs app_label.model
                    if '.' in app_model:
                        app_label, model_name = app_model.split('.')
                        content_types = ContentType.objects.filter(app_label=app_label, model=model_name)
                    else:
                        # Assume it means all models in that app, but restricted actions? 
                        # Or maybe the key IS the app_label?
                        # Let's assume key is app_label for simplicity in this script logic
                        app_label = app_model
                        content_types = ContentType.objects.filter(app_label=app_label)

                    for ct in content_types:
                        for action in actions:
                            codename = f"{action}_{ct.model}"
                            try:
                                perm = Permission.objects.get(content_type=ct, codename=codename)
                                permissions_to_add.append(perm)
                            except Permission.DoesNotExist:
                                self.stdout.write(self.style.WARNING(f"Permission not found: {codename}"))

            group.permissions.set(permissions_to_add)
            self.stdout.write(self.style.SUCCESS(f"Assigned {len(permissions_to_add)} permissions to {role_name}"))

        self.stdout.write(self.style.SUCCESS("Roles setup complete."))
