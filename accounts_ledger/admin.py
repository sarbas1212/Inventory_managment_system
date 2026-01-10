from django.contrib import admin
from accounts_ledger.models import Ledger, LedgerEntry

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ("ledger_name", "ledger_type")
    search_fields = ("ledger_name",)

@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ("ledger", "debit", "credit", "reference", "created_at")
    readonly_fields = (
        "ledger", "debit", "credit",
        "reference", "created_at"
    )

    def has_add_permission(self, request):
        return False
