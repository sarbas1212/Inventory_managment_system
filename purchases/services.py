from django.db import transaction
from decimal import Decimal
from inventory.services import StockService
from accounts_ledger.services import PostingService
from .models import PurchaseItem

class PurchaseService:

    @staticmethod
    @transaction.atomic
    def create_purchase(purchase, items_data):
        from products.models import Product
        from django.db.models import F
        from decimal import Decimal

        # 1️⃣ Save purchase first to get a PK
        purchase.save()

        sub_total = Decimal("0")
        tax_total = Decimal("0")

        for item in items_data:
            product = Product.objects.get(id=item['product_id'])
            qty = Decimal(str(item.get('quantity', 0)))
            price = Decimal(str(item.get('price', 0)))
            tax_percentage = Decimal(str(item.get('tax_percentage', 0)))

            # 2️⃣ Now it's safe to create PurchaseItem
            PurchaseItem.objects.create(
                purchase=purchase,
                product=product,
                quantity=qty,
                price=price,
                tax_percentage=tax_percentage
            )

            line_total = qty * price
            tax_amount = line_total * tax_percentage / Decimal("100")

            sub_total += line_total
            tax_total += tax_amount

            # 3️⃣ Update stock
            StockService.add_stock(
                product=product,
                quantity=qty,
                movement_type="PURCHASE",
                reference=purchase.purchase_number,
                remarks="Purchase from vendor"
            )

        # 4️⃣ Update purchase totals and status
        purchase.sub_total = sub_total
        purchase.tax_amount = tax_total
        purchase.grand_total = sub_total + tax_total - purchase.discount_amount
        purchase.paid_amount = Decimal("0.00")
        purchase.balance_amount = purchase.grand_total
        purchase.status = "DRAFT"  # Or "POSTED" if finalized
        purchase.payment_status = "UNPAID"
        purchase.save()

        # 5️⃣ Ledger posting
        ledger_entries = [
            {'ledger_code': '1004', 'debit': purchase.sub_total, 'credit': 0, 'description': f"Stock from {purchase.purchase_number}"},
            {'ledger_code': '2001', 'debit': 0, 'credit': purchase.grand_total, 'description': f"Liability for {purchase.purchase_number}"}
        ]
        if purchase.tax_amount > 0:
            ledger_entries.append({'ledger_code': '1005', 'debit': purchase.tax_amount, 'credit': 0, 'description': f"VAT on {purchase.purchase_number}"})
        if purchase.discount_amount > 0:
            ledger_entries.append({'ledger_code': '4002', 'debit': 0, 'credit': purchase.discount_amount, 'description': f"Discount on {purchase.purchase_number}"})
        PostingService.post_transaction(
            voucher_type='PURCHASE',
            voucher_number=f"VOU-{purchase.purchase_number}",
            voucher_date=purchase.purchase_date,
            description=f"Purchase from {purchase.vendor.name}",
            entries=ledger_entries
        )

        # 6️⃣ Update vendor outstanding safely
        vendor = purchase.vendor
        vendor.outstanding_balance = F("outstanding_balance") + purchase.grand_total
        vendor.save(update_fields=["outstanding_balance"])

        return purchase

        
    @staticmethod
    @transaction.atomic
    def add_purchase_stock(purchase):
        for item in purchase.items.all():
            StockService.add_stock(
                product=item.product,
                quantity=item.quantity,
                movement_type="PURCHASE",
                reference=purchase.purchase_number,
                remarks="Purchase from Vendor"
            )