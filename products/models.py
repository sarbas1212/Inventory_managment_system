from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel

class Category(TimeStampedModel, SoftDeleteModel):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='children',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Product(TimeStampedModel, SoftDeleteModel):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)

    category = models.ForeignKey(
        Category, null=True, blank=True,
        on_delete=models.SET_NULL
    )

    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    unit = models.CharField(max_length=20, default="pcs")
    reorder_level = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.sku})"
