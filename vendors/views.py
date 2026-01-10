from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Vendor
from .forms import VendorForm 

@login_required
def vendor_list(request):
    vendors = Vendor.objects.filter(is_active=True).order_by("name")
    return render(request, "vendors/vendor_list.html", {"vendors": vendors})
@login_required
def vendor_create(request):
    form = VendorForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                return redirect("vendors:list")
            except IntegrityError:
                form.add_error("phone", "Vendor with this phone number already exists.")
    return render(request, "vendors/vendor_form.html", {"form": form, "title": "Add Vendor"})


@login_required
def vendor_edit(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    form = VendorForm(request.POST or None, instance=vendor)
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                return redirect("vendors:list")
            except IntegrityError:
                form.add_error("phone", "Vendor with this phone number already exists.")
    return render(request, "vendors/vendor_form.html", {"form": form, "title": "Edit Vendor"})


@login_required
def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == "POST":
        vendor.is_active = False
        vendor.save()
        return redirect("vendors:list")
    return render(request, "vendors/vendor_confirm_delete.html", {"vendor": vendor})