from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from invoices.models import SalesInvoice
from purchases.models import Purchase
from inventory.models import Stock
from products.models import Product
from django.utils.timezone import now
from datetime import timedelta


@login_required
def dashboard(request):

    # Total Sales
    total_sales = SalesInvoice.objects.aggregate(total=Sum("grand_total"))["total"] or 0
    total_receivables = SalesInvoice.objects.aggregate(total=Sum("balance_amount"))["total"] or 0
    
    # Total Purchases
    total_purchases = Purchase.objects.aggregate(total=Sum("grand_total"))["total"] or 0
    total_payables = Purchase.objects.aggregate(total=Sum("balance_amount"))["total"] or 0
    
    # Stock Metrics
    total_products = Product.objects.filter(is_active=True).count()
    low_stock_count = Stock.objects.filter(quantity__lt=5).count()
    
    # Recent Transactions
    recent_sales = SalesInvoice.objects.select_related("customer").order_by("-created_at")[:5]
    recent_purchases = Purchase.objects.select_related("vendor").order_by("-created_at")[:5]


    # ================= OVERDUE CALCULATION (NO DB FIELD NEEDED) =================
    today = now().date()
    credit_days = 30

    overdue_invoices = []
    invoices = SalesInvoice.objects.filter(
        payment_status__in=["UNPAID", "PARTIAL"],
        status="POSTED"
    ).select_related("customer")

    for inv in invoices:
        due_date = inv.invoice_date + timedelta(days=credit_days)
        if due_date < today:
            inv.calculated_due_date = due_date
            overdue_invoices.append(inv)

    overdue_invoices = sorted(overdue_invoices, key=lambda x: x.calculated_due_date)[:8]
    # ===========================================================================


    # Time-of-day greeting
    hour = now().hour
    if hour < 12:
        greeting = "morning"
    elif hour < 17:
        greeting = "afternoon"
    else:
        greeting = "evening"

    context = {
        "greeting": greeting,
        "total_sales": total_sales,
        "total_receivables": total_receivables,
        "total_purchases": total_purchases,
        "total_payables": total_payables,
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "recent_sales": recent_sales,
        "recent_purchases": recent_purchases,
        "overdue_invoices": overdue_invoices,
    }
    
    return render(request, "dashboard/dashboard.html", context)
