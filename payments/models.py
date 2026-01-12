from django.db import models
from core.models import TimeStampedModel
from invoices.models import PurchaseInvoice, SalesInvoice
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

    def __str__(self):
        return f"Payment ₹{self.amount}"



