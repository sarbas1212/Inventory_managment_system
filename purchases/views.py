from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Product

from .models import Purchase, PurchaseItem
from .forms import PurchaseForm, PurchaseItemForm
from .services import PurchaseService

@login_required
def purchase_list(request):
    purchases = Purchase.objects.all().order_by("-purchase_date")
    return render(request, "purchases/purchase_list.html", {"purchases": purchases})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal

from products.models import Product
from .models import Purchase, PurchaseItem
from .forms import PurchaseForm
from .services import PurchaseService


@login_required
def purchase_list(request):
    purchases = Purchase.objects.all().order_by("-purchase_date")
    return render(request, "purchases/purchase_list.html", {
        "purchases": purchases
    })


@login_required
@transaction.atomic
def create_purchase(request):
    products = Product.objects.filter(is_active=True).order_by("name")

    if request.method == "POST":
        form = PurchaseForm(request.POST)

        if form.is_valid():
            purchase = form.save(commit=False)

            # Generate Purchase Number
            purchase.purchase_number = f"PUR-{Purchase.objects.count() + 1:04d}"

            purchase.sub_total = Decimal("0.00")
            purchase.tax_amount = Decimal("0.00")
            purchase.grand_total = Decimal("0.00")
            purchase.balance_amount = Decimal("0.00")
            purchase.status = "UNPAID"
            purchase.save()

            sub_total = Decimal("0.00")
            tax_total = Decimal("0.00")

            index = 0
            while True:
                product_id = request.POST.get(f"items[{index}][product_id]")
                if not product_id:
                    break

                product = get_object_or_404(Product, id=product_id)

                qty = Decimal(request.POST.get(f"items[{index}][quantity]", "0"))
                price = Decimal(request.POST.get(f"items[{index}][price]", "0"))
                tax = Decimal(request.POST.get(f"items[{index}][tax_percentage]", "0"))

                PurchaseItem.objects.create(
                    purchase=purchase,
                    product=product,
                    quantity=qty,
                    price=price,
                    tax_percentage=tax
                )

                line_total = qty * price
                tax_amount = line_total * tax / Decimal("100")

                sub_total += line_total
                tax_total += tax_amount

                index += 1

            # Final totals
            purchase.sub_total = sub_total
            purchase.tax_amount = tax_total
            purchase.grand_total = sub_total + tax_total - purchase.discount_amount
            purchase.balance_amount = purchase.grand_total - purchase.paid_amount

            if purchase.balance_amount <= 0:
                purchase.status = "PAID"
            elif purchase.paid_amount > 0:
                purchase.status = "PARTIAL"
            else:
                purchase.status = "UNPAID"

            purchase.save()

            # Update stock
            PurchaseService.add_purchase_stock(purchase)

            return redirect("purchases:list")

    else:
        form = PurchaseForm()

    return render(request, "purchases/purchase_form.html", {
        "form": form,
        "products": products,
        "title": "New Purchase",
    })


@login_required
def edit_purchase(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)

    if request.method == "POST":
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            return redirect("purchases:list")
    else:
        form = PurchaseForm(instance=purchase)

    return render(request, "purchases/purchase_form.html", {
        "form": form,
        "title": "Edit Purchase",
    })