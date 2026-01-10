from django.db import models
from core.models import TimeStampedModel
from customers.models import Customer
from products.models import Product

class Invoice(TimeStampedModel):
    STATUS_CHOICES = (
        ("PAID", "Paid"),
        ("PARTIAL", "Partial"),
        ("UNPAID", "Unpaid"),
    )

    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    invoice_date = models.DateField()

    sub_total = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)

    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.invoice_number


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
