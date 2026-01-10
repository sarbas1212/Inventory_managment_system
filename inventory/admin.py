from django.contrib import admin
from inventory.models import Stock, StockMovement

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "updated_at")
    readonly_fields = ("product", "quantity", "created_at", "updated_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "product", "movement_type",
        "quantity", "reference", "created_at"
    )
    list_filter = ("movement_type",)
    search_fields = ("product__name", "reference")
    readonly_fields = (
        "product", "movement_type", "quantity",
        "reference", "remarks", "created_at"
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
