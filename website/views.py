from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
# Create your views here.

def home(request):
    return render(request, "pages/home.html", {})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Rediriger vers la page de connexion
    else:
        form = SignUpForm()
    return render(request, 'pages/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')
