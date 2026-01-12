from django.contrib import admin
from .models import SalesInvoiceItem,SalesInvoice

class InvoiceItemInline(admin.TabularInline):
    model = SalesInvoiceItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")

@admin.register(SalesInvoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number", "customer",
        "grand_total", "paid_amount",
        "balance_amount", "status"
    )
    list_filter = ("status", "invoice_date")
    search_fields = ("invoice_number", "customer__name")
    inlines = [InvoiceItemInline]
    readonly_fields = (
        "invoice_number", "sub_total",
        "tax_amount", "grand_total",
        "paid_amount", "balance_amount",
        "status"
    )

    def has_delete_permission(self, request, obj=None):
        return False
