from django.contrib import admin
from payments.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "invoice", "amount",
        "payment_method", "payment_date"
    )
    list_filter = ("payment_method",)
    search_fields = ("invoice__invoice_number",)
