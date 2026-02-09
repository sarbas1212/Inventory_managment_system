from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from inventory.models import Stock, StockMovement
from products.models import Product
from .services import StockService

@login_required
def stock_list(request):
    query = request.GET.get("q", "")
    stocks = Stock.objects.select_related("product").all().order_by('-id')

    if query:
        stocks = stocks.filter(
            Q(product__name__icontains(query)) | 
            Q(product__sku__icontains(query))
        )

    paginator = Paginator(stocks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "inventory/stock_list.html", {
        "page_obj": page_obj,
        "query": query
    })

@login_required
def stock_adjustment(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = float(request.POST.get("quantity", 0))
        adj_type = request.POST.get("type") # ADD or REDUCE
        remarks = request.POST.get("remarks")
        
        product = get_object_or_404(Product, id=product_id)
        
        try:
            if adj_type == "ADD":
                StockService.add_stock(
                    product=product,
                    quantity=quantity,
                    movement_type="ADJUSTMENT",
                    remarks=remarks
                )
                messages.success(request, f"Successfully added {quantity} units to {product.name}.")
            else:
                StockService.reduce_stock(
                    product=product,
                    quantity=quantity,
                    movement_type="ADJUSTMENT",
                    remarks=remarks
                )
                messages.success(request, f"Successfully reduced {quantity} units from {product.name}.")
            
            return redirect("inventory:stock_list")
        except ValueError as e:
            messages.error(request, str(e))
            
    products = Product.objects.filter(is_active=True).order_by("name")
    return render(request, "inventory/stock_adjustment.html", {"products": products})

@login_required
def stock_movement_list(request):
    movements = StockMovement.objects.select_related("product").all()
    paginator = Paginator(movements, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "inventory/stock_movement_list.html", {"page_obj": page_obj})

@login_required
def quick_add_stock(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = float(request.POST.get("quantity", 0))
        remarks = request.POST.get("remarks", "Quick adjustment")
        
        product = get_object_or_404(Product, id=product_id)
        
        try:
            StockService.add_stock(
                product=product,
                quantity=quantity,
                movement_type="ADJUSTMENT",
                remarks=remarks
            )
            messages.success(request, f"Successfully added {quantity} units to {product.name}.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            
    return redirect("inventory:stock_list")
