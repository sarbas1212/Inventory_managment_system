from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import SalesInvoice, SalesInvoiceItem
from customers.models import Customer
from products.models import Product
from inventory.services import StockService
from accounts_ledger.services import PostingService

class SalesInvoiceService:
    @staticmethod
    @transaction.atomic
    def create_invoice(data, user=None):
        """
        Creates a Sales Invoice, lines, updates stock, and posts to ledger.
        data: dict containing 'customer_id', 'invoice_date', 'discount_amount', and 'items' (list of dicts)
        """
        from django.db.models import F

        customer_id = data.get("customer_id")
        invoice_date = data.get("invoice_date") or timezone.now().date()
        discount_amount = Decimal(str(data.get("discount_amount", 0)))
        items_data = data.get("items", [])

        if not items_data:
            raise ValueError("No items provided for the invoice.")

        # 1. Create Invoice Header
        invoice = SalesInvoice.objects.create(
            customer_id=customer_id,
            invoice_number=f"INV-{SalesInvoice.objects.count() + 1:04d}",
            invoice_date=invoice_date,
            discount_amount=discount_amount,
            sub_total=0,
            tax_amount=0,
            grand_total=0,
            paid_amount=0,
            balance_amount=0,
            status="UNPAID"
        )

        sub_total = Decimal("0")
        tax_total = Decimal("0")

        # 2. Process Items
        for item in items_data:
            product_id = item.get("product_id")
            qty = Decimal(str(item.get("quantity", 0)))
            price = Decimal(str(item.get("price", 0)))
            tax_percentage = Decimal(str(item.get("tax_percentage", 0)))

            if not product_id or qty <= 0:
                continue

            # Lock product for update
            product = Product.objects.select_for_update().get(id=product_id)

            # Create Invoice Item
            SalesInvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=qty,
                price=price,
                tax_percentage=tax_percentage
            )

            # Reduce Stock
            StockService.reduce_stock(
                product=product,
                quantity=qty,
                movement_type="SALE",
                reference=invoice.invoice_number,
                remarks="Sold via Invoice"
            )

            line_total = qty * price
            line_tax = line_total * (tax_percentage / Decimal("100"))

            sub_total += line_total
            tax_total += line_tax

        # 3. Update Invoice Totals
        invoice.sub_total = sub_total
        invoice.tax_amount = tax_total
        invoice.grand_total = sub_total + tax_total - discount_amount
        invoice.balance_amount = invoice.grand_total
        invoice.save()

        # 4. Double-Entry Posting
        ledger_entries = [
            {
                'ledger_code': '1003',  # Accounts Receivable
                'debit': invoice.grand_total,
                'credit': 0,
                'description': f"Invoice {invoice.invoice_number}"
            },
            {
                'ledger_code': '4001',  # Sales Revenue
                'debit': 0,
                'credit': invoice.sub_total,
                'description': f"Sales Revenue from {invoice.invoice_number}"
            }
        ]

        if invoice.tax_amount > 0:
            ledger_entries.append({
                'ledger_code': '2002',  # Output VAT
                'debit': 0,
                'credit': invoice.tax_amount,
                'description': f"VAT on {invoice.invoice_number}"
            })

        if invoice.discount_amount > 0:
            ledger_entries.append({
                'ledger_code': '5002',  # Sales Discount
                'debit': invoice.discount_amount,
                'credit': 0,
                'description': f"Discount on {invoice.invoice_number}"
            })

        PostingService.post_transaction(
            voucher_type='SALES',
            voucher_number=f"VOU-{invoice.invoice_number}",
            voucher_date=invoice.invoice_date,
            description=f"Sales Invoice {invoice.invoice_number} for {invoice.customer.name}",
            entries=ledger_entries
        )

        # 5. Update Customer Balance using F expression
        customer = invoice.customer
        customer.outstanding_balance = F("outstanding_balance") + invoice.grand_total
        customer.save(update_fields=["outstanding_balance"])

        return invoice
