# payments/services.py
from django.db import transaction
from .models import Payment

class VendorPaymentService:

    @staticmethod
    @transaction.atomic
    def add_payment(
        purchase_invoice,
        amount,
        payment_method,
        transaction_id=None,
        payment_date=None
    ):
        payment = Payment.objects.create(
            purchase_invoice=purchase_invoice,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
            payment_date=payment_date,
        )

        # Update invoice balances
        purchase_invoice.paid_amount += amount
        purchase_invoice.balance_amount = (
            purchase_invoice.grand_total - purchase_invoice.paid_amount
        )

        if purchase_invoice.balance_amount <= 0:
            purchase_invoice.status = "PAID"
            purchase_invoice.balance_amount = 0
        elif purchase_invoice.paid_amount > 0:
            purchase_invoice.status = "PARTIAL"
        else:
            purchase_invoice.status = "UNPAID"

        purchase_invoice.save()

        return payment
