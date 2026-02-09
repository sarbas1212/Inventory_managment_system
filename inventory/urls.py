from django.urls import path
from . import views


app_name = "inventory" 

urlpatterns = [
    path('stock/', views.stock_list, name='stock_list'),
    path('adjustment/', views.stock_adjustment, name='stock_adjustment'),
    path('quick-add/', views.quick_add_stock, name='quick_add'),
    path('movements/', views.stock_movement_list, name='movement_list'),
]
