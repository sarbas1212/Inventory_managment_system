import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_systems.settings')
django.setup()

from products.models import Product
from inventory.models import Stock

def check_orphans():
    print("Checking for Stock entries with inactive Products...")
    
    # 1. Find all Stock entries where product is inactive
    orphan_stocks = Stock.objects.filter(product__is_active=False)
    
    if orphan_stocks.exists():
        print(f"Found {orphan_stocks.count()} Stock entries for inactive products:")
        for stock in orphan_stocks:
            print(f"- Product: {stock.product.name} (SKU: {stock.product.sku}), Quantity: {stock.quantity}")
            
        print("\nFix already applied to view: Filtering by product__is_active=True.")
    else:
        print("No Stock entries for inactive products found (that match the filter).")
        
    # 2. Check "Demo" product specifically
    demo_products = Product.objects.filter(name__icontains="Demo")
    if demo_products.exists():
        print(f"\nFound {demo_products.count()} products matching 'Demo':")
        for p in demo_products:
            print(f"- {p.name} (SKU: {p.sku}), Active: {p.is_active}")
    else:
        print("\nNo product named 'Demo' found.")

if __name__ == "__main__":
    check_orphans()
