from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal
from django.db.models import Q, Sum
from django.core.paginator import Paginator

from products.models import Product
from .models import Purchase, PurchaseItem
from .forms import PurchaseForm
from .services import PurchaseService

@login_required
def purchase_list(request):
    query = request.GET.get("q", "")
    payment_status = request.GET.get("payment_status", "")
    status = request.GET.get("status", "")
    
    purchases = Purchase.objects.all().select_related("vendor")

    if query:
        purchases = purchases.filter(
            Q(purchase_number__icontains=query) |
            Q(vendor__name__icontains=query)
        )
    
    if status is not None and status != "":
         # Check if it's a legacy status or new document status
        if status in ['PAID', 'UNPAID', 'PARTIAL']:
             purchases = purchases.filter(payment_status=status)
        else:
             purchases = purchases.filter(status=status)

    if payment_status:
        purchases = purchases.filter(payment_status=payment_status)

    purchases = purchases.order_by("-purchase_date")
    
    # Calculate totals for the filtered results
    totals = purchases.aggregate(
        total_grand=Sum("grand_total"),
        total_paid=Sum("paid_amount"),
        total_balance=Sum("balance_amount")
    )

    # Pagination
    paginator = Paginator(purchases, 10) # 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "purchases/purchase_list.html", {
        "purchases": page_obj,
        "totals": totals,
        "query": query,
        "status": status,
        "status_choices": Purchase.DOCUMENT_STATUS,
        "payment_status_choices": [('PAID', 'Paid'), ('PARTIAL', 'Partial'), ('UNPAID', 'Unpaid')]
    })

@login_required
def purchase_detail(request, pk):
    purchase = get_object_or_404(Purchase.objects.select_related("vendor"), pk=pk)
    items = purchase.items.all().select_related("product")
    return render(request, "purchases/purchase_detail.html", {
        "purchase": purchase,
        "items": items,
    })

@login_required
@transaction.atomic
def create_purchase(request):
    products = Product.objects.filter(is_active=True).order_by("name")

    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.purchase_number = f"PUR-{Purchase.objects.count() + 1:04d}"

            # Extract items from POST data
            items_data = []
            index = 0
            while True:
                product_id = request.POST.get(f"items[{index}][product_id]")
                if not product_id:
                    break

                items_data.append({
                    'product_id': product_id,
                    'quantity': request.POST.get(f"items[{index}][quantity]", "0"),
                    'price': request.POST.get(f"items[{index}][price]", "0"),
                    'tax_percentage': request.POST.get(f"items[{index}][tax_percentage]", "0"),
                })
                index += 1

            if items_data:
                # Do NOT save here. Let the service handle saving with proper status & totals
                PurchaseService.create_purchase(purchase, items_data)
                return redirect("purchases:list")
            else:
                form.add_error(None, "At least one item is required.")
    else:
        form = PurchaseForm()

    return render(request, "purchases/purchase_form.html", {
        "form": form,
        "products": products,
        "title": "New Purchase",
    })