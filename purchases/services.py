from django.db import transaction
from inventory.services import StockService

class PurchaseService:

    @staticmethod
    @transaction.atomic
    def create_purchase(purchase, items):
        sub_total = 0
        tax_amount = 0

        for item in items:
            qty = item.quantity
            price = item.price
            tax = item.tax_percentage

            line_total = qty * price
            sub_total += line_total
            tax_amount += line_total * tax / 100

            # ✅ Increase stock
            StockService.add_stock(
                product=item.product,
                quantity=qty,
                movement_type="PURCHASE",
                reference=purchase.purchase_number,
                remarks="Purchase from vendor"
            )

        purchase.sub_total = sub_total
        purchase.tax_amount = tax_amount
        purchase.grand_total = sub_total + tax_amount - purchase.discount_amount
        purchase.balance_amount = purchase.grand_total
        purchase.status = "UNPAID"
        purchase.save()

        # ✅ Update vendor outstanding
        vendor = purchase.vendor
        vendor.outstanding_balance += purchase.grand_total
        vendor.save(update_fields=["outstanding_balance"])
        
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