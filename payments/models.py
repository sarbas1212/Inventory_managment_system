from django.db import models
from core.models import TimeStampedModel
from sales.models import Invoice

class Payment(TimeStampedModel):
    PAYMENT_METHODS = (
        ("CASH", "Cash"),
        ("BANK", "Bank Transfer"),
        ("UPI", "UPI"),
        ("CARD", "Card"),
        ("STRIPE", "Stripe"),
    )

    invoice = models.ForeignKey(
        Invoice, related_name="payments",
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateField()
