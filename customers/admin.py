from django.contrib import admin
from customers.models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "credit_limit", "outstanding_balance", "is_active")
    search_fields = ("name", "phone")
    list_filter = ("is_active",)
