# payments/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from invoices.models import PurchaseInvoice
from purchases.models import Purchase
from .models import Payment
from .froms import VendorPaymentForm
from .services import VendorPaymentService
from django.db import transaction

@login_required
def payment_list(request):
    payments = Payment.objects.select_related(
        "sales_invoice",
        "sales_invoice__customer",
        "purchase_invoice",
        "purchase_invoice__vendor",
    ).order_by("-payment_date")

    return render(
        request,
        "payments/payment_list.html",
        {"payments": payments}
    )

@login_required
@transaction.atomic
def add_vendor_payment(request, invoice_id):
    purchase = get_object_or_404(Purchase, id=invoice_id)

    if request.method == "POST":
        form = VendorPaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]

            # Create payment
            Payment.objects.create(
                purchase=purchase,
                amount=amount,
                payment_method=form.cleaned_data["payment_method"],
                transaction_id=form.cleaned_data.get("transaction_id"),
                payment_date=form.cleaned_data["payment_date"],
            )

            # Update purchase totals
            purchase.paid_amount += amount
            purchase.balance_amount = purchase.grand_total - purchase.paid_amount

            if purchase.balance_amount <= 0:
                purchase.status = "PAID"
                purchase.balance_amount = 0
            elif purchase.paid_amount > 0:
                purchase.status = "PARTIAL"
            else:
                purchase.status = "UNPAID"

            purchase.save()

            return redirect("purchases:list")
    else:
        form = VendorPaymentForm()

    return render(request, "payments/vendor_payment_form.html", {
        "form": form,
        "invoice": purchase
    })