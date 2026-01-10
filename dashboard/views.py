from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Only render template, DO NOT call the view inside itself
    return render(request, "dashboard/dashboard.html")
