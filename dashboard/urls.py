from django.urls import path
from . import views

app_name = "dashboard"  # ✅ THIS DEFINES THE NAMESPACE

urlpatterns = [
    path("", views.dashboard, name="dashboard"),  # view function called dashboard
]
