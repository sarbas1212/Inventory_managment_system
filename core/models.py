from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AuditModel(models.Model):
    created_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="created_%(class)s"
    )

    class Meta:
        abstract = True
