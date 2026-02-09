import re
import json
from decimal import Decimal
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Sum
from django.core.paginator import Paginator

from accounts_ledger.services import PostingService
from customers.models import Customer
from products.models import Product
from inventory.services import StockService
from inventory.models import Stock
from payments.models import Payment

from .models import SalesInvoice, SalesInvoiceItem
from .services import SalesInvoiceService


# ===============================
# Invoice List
# ===============================
@login_required
def sales_invoice_list(request):
    query = request.GET.get("q", "")
    status = request.GET.get("status", "")
    payment_status = request.GET.get("payment_status", "")
    
    invoices = SalesInvoice.objects.all().select_related("customer")

    if query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=query) |
            Q(customer__name__icontains=query)
        )
    
    if status:
         # Check if it's a legacy status or new document status
        if status in ['PAID', 'UNPAID', 'PARTIAL']:
             invoices = invoices.filter(payment_status=status)
        else:
             invoices = invoices.filter(status=status)

    if payment_status:
        invoices = invoices.filter(payment_status=payment_status)

    invoices = invoices.order_by("-invoice_date", "-created_at")
    
    # Calculate totals for the filtered results
    totals = invoices.aggregate(
        total_grand=Sum("grand_total"),
        total_paid=Sum("paid_amount"),
        total_balance=Sum("balance_amount")
    )

    # Pagination
    paginator = Paginator(invoices, 10) # 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "invoices/sales_invoice_list.html", {
        "invoices": page_obj,
        "totals": totals,
        "query": query,
        "status": status,
        "status_choices": SalesInvoice.DOCUMENT_STATUS,
        "payment_status_choices": [('PAID', 'Paid'), ('PARTIAL', 'Partial'), ('UNPAID', 'Unpaid')]
    })


# ===============================
# Create Invoice (STOCK SAFE)
# ===============================
@login_required
@transaction.atomic
def create_invoice(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer")
        invoice_date = request.POST.get("invoice_date", date.today())
        discount_amount = Decimal(request.POST.get("discount_amount", "0"))

        # Parse items handling non-consecutive indices
        items_dict = {}
        for key, value in request.POST.items():
            match = re.match(r"items\[(\d+)\]\[(\w+)\]", key)
            if match:
                index = int(match.group(1))
                field = match.group(2)
                if index not in items_dict:
                    items_dict[index] = {}
                items_dict[index][field] = value

        # Convert dict to list
        items_data = [item for _, item in sorted(items_dict.items()) if item.get("product_id")]

        if not items_data:
            messages.error(request, "Please add at least one item.")
            return redirect("invoices:create")

        try:
            invoice = SalesInvoiceService.create_invoice({
                "customer_id": customer_id,
                "invoice_date": invoice_date,
                "discount_amount": discount_amount,
                "items": items_data
            }, user=request.user)
            messages.success(request, f"Invoice {invoice.invoice_number} created successfully.")
            return redirect("invoices:list")
        except Exception as e:
            messages.error(request, f"Error creating invoice: {str(e)}")
            return redirect("invoices:create")

    # ---------- GET ----------
    customers = Customer.objects.all().order_by("name")
    products_qs = Product.objects.select_related("stock").filter(is_active=True)

    products_data = [
        {
            "id": p.id,
            "name": p.name,
            "price": float(p.selling_price),
            "stock": float(p.stock.quantity) if hasattr(p, "stock") else 0,
            "sku": p.sku
        }
        for p in products_qs
    ]

    return render(
        request,
        "invoices/create_sales_invoice.html",
        {
            "customers": customers,
            "products": json.dumps(products_data),
            "today": date.today().isoformat()
        }
    )


# ===============================
# Payment Helper (USED LATER)
# ===============================


@login_required
def sales_invoice_detail(request, pk):
    invoice = get_object_or_404(SalesInvoice.objects.select_related("customer"), pk=pk)
    items = invoice.items.all().select_related("product")
    return render(request, "invoices/sales_invoice_detail.html", {
        "invoice": invoice,
        "items": items,
        "title": f"Invoice {invoice.invoice_number}"
    })
