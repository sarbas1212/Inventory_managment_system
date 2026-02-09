from django.db import transaction
from accounts_ledger.services import PostingService
from .models import Payment

class VendorPaymentService:

    @staticmethod
    @transaction.atomic
    def add_payment(
        purchase,
        amount,
        payment_method,
        transaction_id=None,
        payment_date=None
    ):
        payment = Payment.objects.create(
            purchase=purchase,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
            payment_date=payment_date,
        )

        # Update purchase balances
        purchase.paid_amount += amount
        purchase.balance_amount = purchase.grand_total - purchase.paid_amount

        if purchase.balance_amount <= 0:
            purchase.status = "PAID"
            purchase.balance_amount = 0
        elif purchase.paid_amount > 0:
            purchase.status = "PARTIAL"
        else:
            purchase.status = "UNPAID"

        purchase.save()

        # 🔥 Double-Entry Posting
        payment_ledger = '1001' if payment_method == 'CASH' else '1002'
        PostingService.post_transaction(
        voucher_type='PAYMENT',
        voucher_number=f"PAY-{purchase.purchase_number}-{Payment.objects.count()+1}",
        voucher_date=payment_date or payment.created_at.date(),
        description=f"Payment for Purchase {purchase.purchase_number}",
        entries=[
            {
                'ledger_code': '2001',  # Accounts Payable
                'debit': amount,
                'credit': 0,
                'description': f"Payment to {purchase.vendor.name}"
            },
            {
                'ledger_code': payment_ledger,
                'debit': 0,
                'credit': amount,
                'description': f"Settlement of {purchase.purchase_number}"
            }
        ]
    )

        return payment


class CustomerPaymentService:

    @staticmethod
    @transaction.atomic
    def add_payment(
        sales_invoice,
        amount,
        payment_method,
        transaction_id=None,
        payment_date=None
    ):
        # Create payment
        payment = Payment.objects.create(
            sales_invoice=sales_invoice,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
            payment_date=payment_date
        )

        # Update invoice
        sales_invoice.paid_amount += amount
        sales_invoice.balance_amount = sales_invoice.grand_total - sales_invoice.paid_amount

        if sales_invoice.balance_amount <= 0:
            sales_invoice.status = "PAID"
            sales_invoice.balance_amount = 0
        elif sales_invoice.paid_amount > 0:
            sales_invoice.status = "PARTIAL"
        else:
            sales_invoice.status = "UNPAID"

        sales_invoice.save()

        # Update customer balance
        customer = sales_invoice.customer
        customer.outstanding_balance -= amount
        customer.save()

        # 🔥 Double-Entry Posting
        payment_ledger = '1001' if payment_method == 'CASH' else '1002'
        PostingService.post_transaction(
            voucher_type='RECEIPT',
            voucher_number=f"RCT-{sales_invoice.invoice_number}-{Payment.objects.count()+1}",
            voucher_date=payment_date or payment.created_at.date(),
            description=f"Payment for Invoice {sales_invoice.invoice_number}",
            entries=[
                {
                    'ledger_code': payment_ledger,
                    'debit': amount,
                    'credit': 0,
                    'description': f"Receipt for {sales_invoice.invoice_number}"
                },
                {
                    'ledger_code': '1003', # Accounts Receivable
                    'debit': 0,
                    'credit': amount,
                    'description': f"Payment from {sales_invoice.customer.name}"
                }
            ]
        )

        return payment
