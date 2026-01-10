from django import views
from django.urls import path
from .views import (product_list,
                    product_create,
                    product_delete,
                    product_edit,
                    category_create,
                    category_delete,
                    category_edit,
                    category_list
                    )

app_name = "products" 

urlpatterns = [
    path("", product_list, name="list"),
    path("create/", product_create, name="create"),
    path("<int:pk>/edit/", product_edit, name="edit"),
    path("<int:pk>/delete/", product_delete, name="delete"),

        # Category URLs
    path("categories/", category_list, name="category_list"),
    path("categories/create/", category_create, name="category_create"),
    path("categories/<int:pk>/edit/", category_edit, name="category_edit"),
    path("categories/<int:pk>/delete/", category_delete, name="category_delete"),
]
