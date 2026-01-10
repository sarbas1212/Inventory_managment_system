from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path("", views.sales_invoice_list, name="list"),
    path("create/", views.create_invoice, name="create"),
]
