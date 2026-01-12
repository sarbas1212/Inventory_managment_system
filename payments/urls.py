from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("", views.payment_list, name="list"),
    path("vendor/create/", views.add_vendor_payment, name="vendor_create"),
    path("vendor/<int:invoice_id>/pay/", views.add_vendor_payment, name="add_vendor_payment")
]
