from django.db import models
from core.models import TimeStampedModel
from products.models import Product

class Stock(TimeStampedModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.sku} - {self.quantity}"


class StockMovement(TimeStampedModel):
    MOVEMENT_TYPES = (
        ("OPENING", "Opening Stock"),
        ("PURCHASE", "Purchase"),
        ("SALE", "Sale"),
        ("SALE_RETURN", "Sale Return"),
        ("PURCHASE_RETURN", "Purchase Return"),
        ("DAMAGE", "Damaged"),
        ("ADJUSTMENT", "Adjustment"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
