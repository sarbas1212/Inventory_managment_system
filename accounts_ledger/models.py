from django.db import models
from core.models import TimeStampedModel

class Ledger(TimeStampedModel):
    ledger_name = models.CharField(max_length=255)
    ledger_type = models.CharField(max_length=50)  # CUSTOMER, BANK, CASH, TAX


class LedgerEntry(TimeStampedModel):
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reference = models.CharField(max_length=100)
