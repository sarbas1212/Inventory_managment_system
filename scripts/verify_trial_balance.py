import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_systems.settings')
django.setup()

from accounts_ledger.models import Ledger, LedgerEntry
from django.db.models import Sum

print("=== Trial Balance Verification ===")
ledgers = Ledger.objects.all().order_by('code')
grand_debit = Decimal('0.00')
grand_credit = Decimal('0.00')

print(f"{'Code':<10} {'Name':<30} {'Debit':<15} {'Credit':<15}")
print("-" * 75)

for ledger in ledgers:
    entries = LedgerEntry.objects.filter(ledger=ledger)
    debit = entries.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
    credit = entries.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')
    
    if debit == 0 and credit == 0:
        continue
        
    print(f"{ledger.code:<10} {ledger.name:<30} {debit:<15} {credit:<15}")
    grand_debit += debit
    grand_credit += credit

print("-" * 75)
print(f"{'TOTAL':<41} {grand_debit:<15} {grand_credit:<15}")

diff = grand_debit - grand_credit
if diff == 0:
    print("\n✅ TRIAL BALANCE MATCHED! System is balanced.")
else:
    print(f"\n❌ TRIAL BALANCE MISMATCH! Difference: {diff}")
