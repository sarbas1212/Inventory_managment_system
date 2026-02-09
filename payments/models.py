from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from core.models import TimeStampedModel
from invoices.models import SalesInvoice
from purchases.models import Purchase
from vendors.models import Vendor

class Payment(TimeStampedModel):
    PAYMENT_METHODS = (
        ("CASH", "Cash"),
        ("BANK", "Bank Transfer"),
        ("UPI", "UPI"),
        ("CARD", "Card"),
        ("STRIPE", "Stripe"),
    )

    sales_invoice = models.ForeignKey(
        SalesInvoice, null=True, blank=True,
        on_delete=models.CASCADE
    )
    purchase = models.ForeignKey(
        Purchase, null=True, blank=True,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateField()

    def clean(self):
        if self.sales_invoice and self.purchase:
            raise ValidationError("Payment cannot be linked to both Sales Invoice and Purchase.")
        if not self.sales_invoice and not self.purchase:
            raise ValidationError("Payment must be linked to either Sales Invoice or Purchase.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment ₹{self.amount}"

    class Meta:
        constraints = [
            models.CheckConstraint(
            condition=(
                Q(sales_invoice__isnull=False) & Q(purchase__isnull=True)
            ) | (
                Q(sales_invoice__isnull=True) & Q(purchase__isnull=False)
            ),
            name="payment_must_link_to_one_document"
        )
        ]
    
