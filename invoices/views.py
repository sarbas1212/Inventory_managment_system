from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from customers.models import Customer
from products.models import Product
from inventory.services import StockService
from inventory.models import Stock
from payments.models import Payment

from .models import SalesInvoice,SalesInvoiceItem


# ===============================
# Invoice List
# ===============================
@login_required
def sales_invoice_list(request):
    invoices = SalesInvoice.objects.select_related("customer").order_by("-invoice_date")
    return render(
        request,
        "invoices/sales_invoice_list.html",
        {"invoices": invoices}
    )


# ===============================
# Create Invoice (STOCK SAFE)
# ===============================
@login_required
@transaction.atomic
def create_invoice(request):

    # ---------- POST ----------
    if request.method == "POST":
        customer_id = request.POST.get("customer")

        products = request.POST.getlist("product[]")
        quantities = request.POST.getlist("quantity[]")
        prices = request.POST.getlist("price[]")
        taxes = request.POST.getlist("tax[]")

        # Create Invoice (initial)
        invoice = SalesInvoice.objects.create(
            customer_id=customer_id,
            invoice_number=f"INV-{SalesInvoice.objects.count() + 1}",
            invoice_date=date.today(),
            sub_total=0,
            tax_amount=0,
            discount_amount=0,
            grand_total=0,
            paid_amount=0,
            balance_amount=0,
            status="UNPAID"
        )

        sub_total = 0
        tax_total = 0

        # Loop through items
        for i in range(len(products)):
            product = Product.objects.select_for_update().get(id=products[i])
            qty = float(quantities[i])
            price = float(prices[i])
            tax = float(taxes[i])

            # Create Invoice Item
            SalesInvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=qty,
                price=price,
                tax_percentage=tax
            )

            # 🔥 Reduce Stock (ATOMIC)
            StockService.reduce_stock(
                product=product,
                quantity=qty,
                movement_type="SALE",
                reference=invoice.invoice_number,
                remarks="Sold via Invoice"
            )

            line_total = qty * price
            line_tax = line_total * tax / 100

            sub_total += line_total
            tax_total += line_tax

        # Final totals
        invoice.sub_total = sub_total
        invoice.tax_amount = tax_total
        invoice.grand_total = sub_total + tax_total - invoice.discount_amount
        invoice.balance_amount = invoice.grand_total
        invoice.save()

        return redirect("invoices:list")

    # ---------- GET ----------
    customers = Customer.objects.all()

    products_qs = Product.objects.select_related("stock").all()

    products_data = [
        {
            "id": p.id,
            "name": p.name,
            "price": float(p.selling_price),
            "stock": float(p.stock.quantity) if hasattr(p, "stock") else 0
        }
        for p in products_qs
    ]

    return render(
        request,
        "invoices/create_sales_invoice.html",
        {
            "customers": customers,
            "products": products_data
        }
    )


# ===============================
# Payment Helper (USED LATER)
# ===============================
def add_payment_to_invoice(invoice, amount, method, transaction_id=None, payment_date=None):
    if payment_date is None:
        payment_date = date.today()

    with transaction.atomic():
        Payment.objects.create(
            invoice=invoice,
            amount=amount,
            payment_method=method,
            transaction_id=transaction_id,
            payment_date=payment_date
        )

        invoice.paid_amount += amount
        invoice.balance_amount = invoice.grand_total - invoice.paid_amount

        if invoice.balance_amount <= 0:
            invoice.status = "PAID"
            invoice.balance_amount = 0
        elif invoice.paid_amount > 0:
            invoice.status = "PARTIAL"
        else:
            invoice.status = "UNPAID"

        invoice.save()
