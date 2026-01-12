from datetime import date
from django.db import transaction
from inventory.services import StockService
from .models import SalesInvoice, SalesInvoiceItem
from products.models import Product
from models import PurchaseInvoice, PurchaseInvoiceItem




class SalesInvoiceService:

    @staticmethod
    @transaction.atomic
    def create_sales_invoice(customer_id, items):
        invoice = SalesInvoice.objects.create(
            customer_id=customer_id,
            invoice_number=f"INV-{SalesInvoice.objects.count() + 1}",
            invoice_date=date.today(),
            sub_total=0,
            tax_amount=0,
            discount_amount=0,
            grand_total=0,
            paid_amount=0,
            balance_amount=0,
            status="UNPAID"
        )

        sub_total = 0
        tax_total = 0

        for item in items:
            product = Product.objects.select_for_update().get(id=item["product"])
            qty = item["quantity"]
            price = item["price"]
            tax = item["tax"]

            SalesInvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=qty,
                price=price,
                tax_percentage=tax
            )

            # 🔥 Reduce stock
            StockService.reduce_stock(
                product=product,
                quantity=qty,
                movement_type="SALE",
                reference=invoice.invoice_number,
                remarks="Sold via Invoice"
            )

            line_total = qty * price
            tax_total += line_total * tax / 100
            sub_total += line_total

        invoice.sub_total = sub_total
        invoice.tax_amount = tax_total
        invoice.grand_total = sub_total + tax_total
        invoice.balance_amount = invoice.grand_total
        invoice.save()

        return invoice


class PurchaseInvoiceService:

    @staticmethod
    @transaction.atomic
    def create_purchase_invoice(vendor_id, items):
        invoice = PurchaseInvoice.objects.create(
            vendor_id=vendor_id,
            invoice_number=f"PINV-{PurchaseInvoice.objects.count() + 1}",
            invoice_date=date.today(),
            sub_total=0,
            tax_amount=0,
            discount_amount=0,
            grand_total=0,
            paid_amount=0,
            balance_amount=0,
            status="UNPAID"
        )

        sub_total = 0
        tax_total = 0

        for item in items:
            product = Product.objects.select_for_update().get(id=item["product"])
            qty = item["quantity"]
            price = item["price"]
            tax = item["tax"]

            PurchaseInvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=qty,
                price=price,
                tax_percentage=tax
            )

            # 🔥 Add stock
            StockService.add_stock(
                product=product,
                quantity=qty,
                movement_type="PURCHASE",
                reference=invoice.invoice_number,
                remarks="Purchased from Vendor"
            )

            line_total = qty * price
            tax_total += line_total * tax / 100
            sub_total += line_total

        invoice.sub_total = sub_total
        invoice.tax_amount = tax_total
        invoice.grand_total = sub_total + tax_total
        invoice.balance_amount = invoice.grand_total
        invoice.save()

        return invoice
