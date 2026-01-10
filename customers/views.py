from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import CustomerForm
from .models import Customer



@login_required
def customer_list(request):
    customers = Customer.objects.filter(is_active=True).order_by("name")
    return render(
        request,
        "customers/customer_list.html",
        {"customers": customers}
    )

@login_required
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customers:list")
    else:
        form = CustomerForm()

    return render(
        request,
        "customers/customer_form.html",
        {"form": form, "title": "Add Customer"}
    )


@login_required
def customer_edit(request, pk):
    customer = Customer.objects.get(pk=pk, is_active=True)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("customers:list")
    else:
        form = CustomerForm(instance=customer)

    return render(
        request,
        "customers/customer_form.html",
        {"form": form, "title": "Edit Customer"}
    )




@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(
        Customer,
        id=pk,
        is_active=True
    )

    if request.method == "POST":
        customer.is_active = False
        customer.save(update_fields=["is_active"])
        return redirect("customers:list")

    return redirect("customers:list")