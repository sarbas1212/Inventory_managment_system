from django.urls import path
from . import views

app_name = "purchases"

urlpatterns = [
    path("", views.purchase_list, name="list"),
    path("create/", views.create_purchase, name="create"),
    path("<int:pk>/", views.purchase_detail, name="detail"),
]
