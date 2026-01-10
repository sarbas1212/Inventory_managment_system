from django.db import transaction
from django.db.models import F
from inventory.models import Stock, StockMovement

class StockService:

    @staticmethod
    @transaction.atomic
    def add_stock(product, quantity, movement_type, reference=None, remarks=None):
        stock, _ = Stock.objects.select_for_update().get_or_create(
            product=product,
            defaults={"quantity": 0}
        )

        StockMovement.objects.create(
            product=product,
            movement_type=movement_type,
            quantity=quantity,
            reference=reference,
            remarks=remarks
        )

        stock.quantity = F("quantity") + quantity
        stock.save(update_fields=["quantity"])

    @staticmethod
    @transaction.atomic
    def reduce_stock(product, quantity, movement_type, reference=None, remarks=None):
        stock = Stock.objects.select_for_update().get(product=product)

        if stock.quantity < quantity:
            raise ValueError("Insufficient stock")

        StockMovement.objects.create(
            product=product,
            movement_type=movement_type,
            quantity=-quantity,
            reference=reference,
            remarks=remarks
        )

        stock.quantity = F("quantity") - quantity
        stock.save(update_fields=["quantity"])
