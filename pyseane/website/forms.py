from django import forms
from .models import campagne_fish

class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'minlength': 3}),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'minlength': 8}),
        required=True
    )
    accept_terms = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=True
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
        required=True
    )


class CampagneForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
        required=True
    )
    url = forms.URLField(
        label='URL',
        required=True,
        widget=forms.URLInput(attrs={'class': 'form-control form-control-lg'})
    )
    
class CampagneUtilisateurForm(forms.Form):
    def __init__(self, utilisateur, selected_campagne_id, *args, **kwargs):
        super(CampagneUtilisateurForm, self).__init__(*args, **kwargs)
        campagnes = campagne_fish.objects.filter(utilisateur=utilisateur)
        
        self.fields['campagne'] = forms.ModelChoiceField(
            queryset=campagnes,
            empty_label=None,
            widget=forms.Select(attrs={'onchange': 'this.form.submit();'}),
            initial=selected_campagne_id
        )




