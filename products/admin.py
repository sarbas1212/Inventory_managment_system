from django.contrib import admin

# Register your models here.
from django.contrib import admin
from products.models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name", "sku", "category",
        "selling_price", "reorder_level", "is_active"
    )
    search_fields = ("name", "sku")
    list_filter = ("category", "is_active")
    readonly_fields = ("created_at", "updated_at")
