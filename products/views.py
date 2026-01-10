from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from inventory.services import StockService
from .models import Category, Product
from .forms import CategoryForm, ProductForm

@login_required
def product_list(request):
    products = Product.objects.filter(is_active=True).order_by("name")
    return render(request, "products/product_list.html", {"products": products})

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            opening_stock = form.cleaned_data.pop("opening_stock", 0)
            product = form.save()

            # ✅ Add opening stock if provided
            if opening_stock and opening_stock > 0:
                StockService.add_stock(
                    product=product,
                    quantity=opening_stock,
                    movement_type="OPENING",
                    remarks="Opening stock on product creation"
                )

            return redirect("products:list")
    else:
        form = ProductForm()

    return render(request, "products/product_form.html", {
        "form": form,
        "title": "Add Product"
    })

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products:list")
    else:
        form = ProductForm(instance=product)
    return render(request, "products/product_form.html", {"form": form, "title": "Edit Product"})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    if request.method == "POST":
        product.is_active = False
        product.save()
        return redirect("products:list")
    return render(request, "products/product_confirm_delete.html", {"product": product})



@login_required
def category_list(request):
    # Check if "parent_only" query parameter exists
    parent_only = request.GET.get("parent_only", None)

    if parent_only == "1":
        # Only top-level categories
        categories = Category.objects.filter(is_active=True, parent=None).order_by("name")
    else:
        # All categories
        categories = Category.objects.filter(is_active=True).order_by("name")

    return render(request, "products/category_list.html", {
        "categories": categories,
        "parent_only": parent_only
    })

@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products:category_list")
    else:
        form = CategoryForm()
    return render(request, "products/category_form.html", {"form": form, "title": "Add Category"})

@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk, is_active=True)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("products:category_list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "products/category_form.html", {"form": form, "title": "Edit Category"})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, is_active=True)
    if request.method == "POST":
        category.is_active = False
        category.save()
        return redirect("products:category_list")
    return render(request, "products/category_confirm_delete.html", {"category": category})