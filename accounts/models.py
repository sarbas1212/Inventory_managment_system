from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'System Administrator'),
        ('ACCOUNTANT', 'Senior Accountant'),
        ('STAFF', 'Data Entry Staff'),
        ('VIEWER', 'ReadOnly Viewer'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser

    def is_accountant(self):
        return self.role in ['ADMIN', 'ACCOUNTANT']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
