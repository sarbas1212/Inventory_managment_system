# payments/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from invoices.models import SalesInvoice
from purchases.models import Purchase
from .models import Payment
from .froms import CustomerPaymentForm, VendorPaymentForm
from .services import CustomerPaymentService, VendorPaymentService
from django.db import transaction

@login_required
def payment_list(request):
    payments = Payment.objects.select_related(
        "sales_invoice",
        "sales_invoice__customer",
        "purchase",
        "purchase__vendor",
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

            # Use service for payment and ledger posting
            VendorPaymentService.add_payment(
                purchase=purchase,
                amount=amount,
                payment_method=form.cleaned_data["payment_method"],
                transaction_id=form.cleaned_data.get("transaction_id"),
                payment_date=form.cleaned_data["payment_date"],
            )

            return redirect("purchases:list")
        else:
            print("VENDOR PAYMENT FORM ERRORS:", form.errors)  
    else:
        form = VendorPaymentForm()

    return render(request, "payments/vendor_payment_form.html", {
        "form": form,
        "invoice": purchase
    })



@login_required
def add_customer_payment(request, invoice_id):
    invoice = get_object_or_404(SalesInvoice, id=invoice_id)

    if request.method == "POST":
        form = CustomerPaymentForm(request.POST)
        if form.is_valid():
            CustomerPaymentService.add_payment(
                sales_invoice=invoice,
                amount=form.cleaned_data["amount"],
                payment_method=form.cleaned_data["payment_method"],
                transaction_id=form.cleaned_data.get("transaction_id"),
                payment_date=form.cleaned_data["payment_date"],
            )
            return redirect("invoices:list")
        else:
            print("CUSTOMER PAYMENT FORM ERRORS:", form.errors)  
    else:
        form = CustomerPaymentForm()

    return render(
        request,
        "payments/customer_payment_form.html",
        {
            "form": form,
            "invoice": invoice,
        }
    )