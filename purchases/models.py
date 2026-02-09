from django.db import models
from core.models import TimeStampedModel
from vendors.models import Vendor
from products.models import Product

class Purchase(TimeStampedModel):
    DOCUMENT_STATUS = (
        ("DRAFT", "Draft"),
        ("POSTED", "Posted"),
        ("CANCELLED", "Cancelled"),
    )

    purchase_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    purchase_date = models.DateField()

    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=15, choices=DOCUMENT_STATUS, default="DRAFT")
    
    # Financial Status (denormalized)
    payment_status = models.CharField(
        max_length=10, 
        choices=(("PAID", "Paid"), ("PARTIAL", "Partial"), ("UNPAID", "Unpaid")),
        default="UNPAID"
    )


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase, related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def line_total(self):
        return self.quantity * self.price + (self.quantity * self.price * self.tax_percentage / 100)
