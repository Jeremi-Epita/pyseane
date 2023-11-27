from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import Pyseane_User, campagne_fish
from .forms import RegistrationForm, LoginForm, CampagneForm
from .module.Pywebcloner import clone

def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        campagnes = campagne_fish.objects.filter(utilisateur=request.user)
        if campagnes:
            return redirect(panel)
        else:
            return redirect(campagne_register)
    else:
        return redirect(login_user)

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

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(login_user)

def campagne_register(request):
    if request.method == 'GET':
        form = CampagneForm()
        return render(request, 'pages/campagne.html', {'form': form})
    elif request.method == 'POST':
        form = CampagneForm(data=request.POST)
        if form.is_valid():
            nom_campagne = form.cleaned_data.get('name')
            url_campagne = form.cleaned_data.get('url')
            nouvelle_campagne = campagne_fish.objects.create(
                utilisateur=request.user,
                nom=nom_campagne,
                url=url_campagne
            )
            # TODO verifier si la campagne existe deja ? pas obligatoire
            nouvelle_campagne.save()
            clone(nouvelle_campagne.id,url_campagne)

            return redirect(panel)

    return HttpResponse("Méthode non supportée.", status=405)

def detail_campagne(request, id):
    campagnes = campagne_fish.objects.get(id=id)
    user_camp = campagnes.utilisateur.username
    if user_camp == request.user.username:
        return render(request, "pages/pages_fishing/"+str(campagnes.id)+".html")
    else:
        return HttpResponse("Vous n'avez pas le droit de voir ceci.", status=403)

def panel(request):
    if request.user.is_authenticated:
        campagne_id = request.GET.get('id')
        #TODO add trycatch pour invalid uuid
        if campagne_id:
            selected_campagne = campagne_fish.objects.get(id=campagne_id)
        else:
            selected_campagne = campagne_fish.objects.filter(utilisateur=request.user).first()
            return redirect("/panel?id="+str(selected_campagne.id))
        context = {
            'username': request.user.username,
            'email': request.user.email,
            'selected_campagne': selected_campagne,
        }
        if request.user.username == selected_campagne.utilisateur.username:
            return render(request, 'pages/panel.html', context)
        else:
            return HttpResponse("Vous n'avez pas le droit de voir ceci.", status=403)
    else:
        return redirect(home)