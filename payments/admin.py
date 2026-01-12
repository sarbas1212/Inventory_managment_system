from django.contrib import admin
from payments.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invoice_number",
        "invoice_type",
        "amount",
        "payment_method",
        "payment_date",
    )

    list_filter = ("payment_method", "payment_date")
    search_fields = (
        "sales_invoice__invoice_number",
        "purchase_invoice__purchase_number",
    )

    def invoice_number(self, obj):
        if obj.sales_invoice:
            return obj.sales_invoice.invoice_number
        if obj.purchase_invoice:
            return obj.purchase_invoice.purchase_number
        return "-"

    def invoice_type(self, obj):
        if obj.sales_invoice:
            return "Sales"
        if obj.purchase_invoice:
            return "Purchase"
        return "-"

    invoice_number.short_description = "Invoice No"
    invoice_type.short_description = "Type"