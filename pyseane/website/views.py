import hashlib

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from .models import Pyseane_User, campagne_fish,target
from .forms import RegistrationForm, LoginForm, CampagneForm, EmailForm
from .module.Pywebcloner import clone
from .module.Emailsender import EmailSender
from .forms import CampagneUtilisateurForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count



def home(request):
    if request.user.is_authenticated:
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
                response = redirect('login_user')
                response.delete_cookie('campagne_id')
                return response
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

@csrf_exempt
def detail_campagne(request, id):
    target_id = request.GET.get('follow')
    campagnes = campagne_fish.objects.get(id=id)
    if request.method == 'GET':
        if target_id:
            try:
                ma_target = target.objects.get(id_email_hashed=target_id)
                if not ma_target.has_open:
                    ma_target.has_open = True
                    ma_target.save()
                else: # PERMET DE DEBUG en resetant
                   ma_target.has_open = False
                   ma_target.save()
            except Exception:
              return render(request, "pages/pages_fishing/" + str(campagnes.id) + ".html")
        return render(request, "pages/pages_fishing/"+str(campagnes.id)+".html")

    elif request.method == 'POST':
        return render(request, "pages/pages_fishing/"+str(campagnes.id)+".html")


def panel(request):
    if request.user.is_authenticated:
        campagne_id = request.COOKIES.get('campagne_id', 'null')

        # Récupérer la campagne actuellement sélectionnée
        if campagne_id == "null":
            selected_campagne = campagne_fish.objects.filter(utilisateur=request.user).first()
            if selected_campagne:
                response = redirect("panel")
                response.set_cookie('campagne_id', str(selected_campagne.id))
                return response

        if 'campagne' in request.GET:
            form = CampagneUtilisateurForm(request.user, campagne_id, request.GET)
            if form.is_valid():
                selected_campagne = form.cleaned_data['campagne']
                response = redirect("panel")
                response.set_cookie('campagne_id', str(selected_campagne.id))
                return response
        else:
            # Le formulaire n'est pas soumis, initialisez-le sans données
            form = CampagneUtilisateurForm(request.user, campagne_id)
        selected_campagne = campagne_fish.objects.get(id=campagne_id)
        context = {
            'username': request.user.username,
            'email': request.user.email,
            'selected_campagne': selected_campagne,
            'form': form,
            'all_campagnes' : campagne_fish.objects.filter(utilisateur=request.user)
        }

        if request.user.username == selected_campagne.utilisateur.username:
            return render(request, 'pages/panel.html', context)
        else:
            return HttpResponse("Vous n'avez pas le droit de voir ceci.", status=403)
    else:
        return redirect(home)


def email(request):
    if request.user.is_authenticated:
        campagne_id = request.COOKIES.get('campagne_id', 'null')

        if campagne_id != "null":
            selected_campagne = campagne_fish.objects.get(id=campagne_id)
        else:
            #TODO forcer user a choisir la campagne
            selected_campagne = campagne_fish.objects.filter(utilisateur=request.user).first()
            response = redirect("/panel/email")
            response.set_cookie('campagne_id', str(selected_campagne.id))
            return response

        if request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                receiver = form.cleaned_data['receiver'].replace('\r', '').split('\n')
                subject = form.cleaned_data['subject']
                content = form.cleaned_data['content']

                sended = EmailSender(str(selected_campagne.id), name, receiver, subject, content)

                for c in sended:
                    nouvelle_target = target.objects.create(
                    id_email_hashed=hashlib.sha256(c.encode()).hexdigest(),
                    campagne=selected_campagne,
                    )
                    nouvelle_target.save()
                return redirect(email)
        else:
            form = EmailForm()
        targets_for_campagne = target.objects.filter(campagne=selected_campagne)
        context = {
            'username': request.user.username,
            'email': request.user.email,
            'selected_campagne': selected_campagne,
            'targets_for_campagne': targets_for_campagne,
            'form': form,  # Ajoutez le formulaire au contexte
        }

        if request.user.username == selected_campagne.utilisateur.username:
            return render(request, 'pages/email.html', context)
        else:
            return HttpResponse("Vous n'avez pas le droit de voir ceci.", status=403)
    else:
        return redirect(home)

def gestion_campagne(request):
    if request.user.is_authenticated:
        campagne_id = request.COOKIES.get('campagne_id', 'null')
        if campagne_id != "null":
            selected_campagne = campagne_fish.objects.get(id=campagne_id)
        else:
            selected_campagne = campagne_fish.objects.filter(utilisateur=request.user).first()
            response = redirect("/panel/campagnes")
            response.set_cookie('campagne_id', str(selected_campagne.id))
            return response

        all_campagne = campagne_fish.objects.filter(utilisateur=request.user)
        form = CampagneUtilisateurForm(request.user, campagne_id)
        context = {
            'username': request.user.username,
            'email': request.user.email,
            'campagnes': all_campagne,
            'form': form
        }
        if request.user.username == selected_campagne.utilisateur.username:
            return render(request, 'pages/gestion_campagne.html', context)
        else:
            return HttpResponse("Vous n'avez pas le droit de voir ceci.", status=403)
    else:
        return redirect(home)
