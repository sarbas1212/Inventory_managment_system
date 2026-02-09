from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "pages"

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='pages:home'), name='logout'),
    path('register/', views.register, name='register'),
]
