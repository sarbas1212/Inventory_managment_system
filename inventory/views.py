from django.shortcuts import render
from inventory.models import Stock

def stock_list(request):
    stocks = Stock.objects.select_related("product")
    return render(request, "inventory/stock_list.html", {"stocks": stocks})
