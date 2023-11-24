from django.shortcuts import render, redirect
from .forms import SignUpForm

def register(request):
    return render(request, 'pages/register.html')
