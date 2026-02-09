from django.contrib import admin
from accounts_ledger.models import Ledger, LedgerEntry, Voucher

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "ledger_type")
    search_fields = ("name", "code")

class LedgerEntryInline(admin.TabularInline):
    model = LedgerEntry
    extra = 0
    readonly_fields = ("ledger", "debit", "credit", "description")

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ("voucher_number", "voucher_date", "voucher_type", "is_posted")
    list_filter = ("voucher_type", "is_posted")
    search_fields = ("voucher_number", "description")
    inlines = [LedgerEntryInline]

@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ("ledger", "voucher", "debit", "credit", "created_at")
    list_filter = ("ledger", "created_at")
    readonly_fields = ("ledger", "voucher", "debit", "credit", "description", "created_at")

    def has_add_permission(self, request):
        return False
