from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Payment

@login_required
def payment_list(request):
    payments = Payment.objects.select_related("invoice", "invoice__customer").order_by("-payment_date")
    return render(request, "payments/payment_list.html", {"payments": payments})
