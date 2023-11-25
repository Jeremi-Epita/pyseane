from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import Pyseane_User
from .forms import RegistrationForm, LoginForm

def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        return HttpResponse(f"Connecté en tant que {username}, adresse e-mail : {email}")
    else:
        # L'utilisateur n'est pas connecté
        return redirect(login)

def cgu(request):
    return render(request, 'pages/cgu.html')

def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'pages/register.html', {'form': form})
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            accept_terms = form.cleaned_data['accept_terms']

            if len(username) < 3 or len(password) < 8:
                return HttpResponse("Le nom d'utilisateur doit comporter au moins 3 caractères et le mot de passe au moins 8 caractères.",status=400)
            elif accept_terms != True:
                return HttpResponse("Vous devez accepter les Conditions Générales d'Utilisation.", status=403)
            else:
                Pyseane_User.objects.create_user(username=username, email=email, password=password)
                #TODO  faire un trycatch pour les erreurs
                if not request.session.get('success_message_displayed', False):
                    messages.success(request, 'Inscription réussie ! Connectez-vous avec votre nouveau compte.')
                    request.session['success_message_displayed'] = True
                return render(request, 'pages/register.html', {'form': form})

    else:
        return HttpResponse("Méthode non supportée.", status=405)

def login_user(request):
    if request.method == 'POST':
        print(request.POST)
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('login_user')
            else:
                form.add_error(None, 'Nom d\'utilisateur ou mot de passe incorrect.')
    elif request.user.is_authenticated:
        return redirect(home)
    else:
        form = LoginForm()

    return render(request, 'pages/login.html', {'form': form})