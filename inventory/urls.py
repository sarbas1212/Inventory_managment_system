from django.urls import path
from .views import stock_list


app_name = "inventory" 

urlpatterns = [
    path('stock/', stock_list, name='stock_list'),
]
