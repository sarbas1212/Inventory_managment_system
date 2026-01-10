from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel

class Vendor(TimeStampedModel, SoftDeleteModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    gst_number = models.CharField(max_length=30, blank=True, null=True)

    address = models.TextField()
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name
