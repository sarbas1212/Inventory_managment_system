from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product
from inventory.models import Stock

@receiver(post_save, sender=Product)
def create_stock(sender, instance, created, **kwargs):
    if created:
        Stock.objects.create(product=instance)
