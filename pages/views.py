from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    """Public home page"""
    return render(request, 'pages/home.html')

def about(request):
    """Public about page"""
    return render(request, 'pages/about.html')

def contact(request):
    """Public contact page"""
    return render(request, 'pages/contact.html')


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now login.')
            return redirect('pages:login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserCreationForm()
    return render(request, 'pages/register.html', {'form': form})
