from django.db import models
from core.models import TimeStampedModel
from django.core.exceptions import ValidationError

class Ledger(TimeStampedModel):
    LEDGER_TYPES = (
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('EQUITY', 'Equity'),
        ('REVENUE', 'Revenue'),
        ('EXPENSE', 'Expense'),
    )
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=20, unique=True)
    ledger_type = models.CharField(max_length=20, choices=LEDGER_TYPES)
    
    def get_balance(self):
        entries = self.entries.all()
        debit_total = sum(e.debit for e in entries)
        credit_total = sum(e.credit for e in entries)
        return debit_total - credit_total

    def __str__(self):
        return f"{self.code} - {self.name}"

class Voucher(TimeStampedModel):
    VOUCHER_TYPES = (
        ('RECEIPT', 'Receipt'),
        ('PAYMENT', 'Payment'),
        ('JOURNAL', 'Journal'),
        ('SALES', 'Sales'),
        ('PURCHASE', 'Purchase'),
    )
    voucher_number = models.CharField(max_length=50, unique=True)
    voucher_date = models.DateField()
    voucher_type = models.CharField(max_length=20, choices=VOUCHER_TYPES)
    description = models.TextField(blank=True)
    is_posted = models.BooleanField(default=False)

    def clean(self):
        # Ensure debits == credits before posting
        if self.is_posted:
            entries = self.entries.all()
            debit_sum = sum(e.debit for e in entries)
            credit_sum = sum(e.credit for e in entries)
            if debit_sum != credit_sum:
                raise ValidationError(f"Cannot post unbalanced voucher: Debit ({debit_sum}) != Credit ({credit_sum})")

    def save(self, *args, **kwargs):
        if self.is_posted:
            self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.voucher_number

class LedgerEntry(TimeStampedModel):
    ledger = models.ForeignKey(Ledger, related_name='entries', on_delete=models.PROTECT)
    voucher = models.ForeignKey(Voucher, related_name='entries', on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.ledger.name} | DR: {self.debit} | CR: {self.credit}"
