from django.contrib import admin
from vendors.models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "outstanding_balance", "is_active")
    search_fields = ("name", "phone")
