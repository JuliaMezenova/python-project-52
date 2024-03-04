from django import forms
from .users.models import User
# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Name of user'), widget=forms.TextInput)
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']
