from decimal import Decimal
from django.db import transaction
from .models import Voucher, LedgerEntry, Ledger

class PostingService:
    @staticmethod
    @transaction.atomic
    def post_transaction(voucher_type, voucher_number, voucher_date, description, entries):
        """
        entries format: [{'ledger_code': '1001', 'debit': 100, 'credit': 0, 'description': '...'}, ...]
        """
        voucher = Voucher.objects.create(
            voucher_type=voucher_type,
            voucher_number=voucher_number,
            voucher_date=voucher_date,
            description=description
        )

        for entry_data in entries:
            ledger = Ledger.objects.get(code=entry_data['ledger_code'])
            LedgerEntry.objects.create(
                voucher=voucher,
                ledger=ledger,
                debit=Decimal(str(entry_data.get('debit', 0))),
                credit=Decimal(str(entry_data.get('credit', 0))),
                description=entry_data.get('description', '')
            )

        # Validate balance before finalizing
        voucher.clean()
        voucher.is_posted = True
        voucher.save()
        return voucher

    @staticmethod
    def get_or_create_ledger(code, name, ledger_type):
        ledger, created = Ledger.objects.get_or_create(
            code=code,
            defaults={'name': name, 'ledger_type': ledger_type}
        )
        return ledger
