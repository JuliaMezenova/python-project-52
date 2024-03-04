from django import forms
from django.forms import ModelForm
from .models import User
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label=_('Name'), widget=forms.TextInput)
    last_name = forms.CharField(label=_('Surname'), widget=forms.TextInput)
    username = forms.CharField(label=_('Name of user'), widget=forms.TextInput)
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)
    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )


#class UserLoginForm(AuthenticationForm):
#    username = forms.CharField(label=_('Name of user'), widget=forms.TextInput)
#    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
#    class Meta:
#        model = User
#        fields = ('username', 'password')
