from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label=_('Name'), widget=forms.TextInput)
    last_name = forms.CharField(label=_('Surname'), widget=forms.TextInput)
    username = forms.CharField(
        label=_('Name of user'),
        widget=forms.TextInput,
        help_text=_("The username must contain only letters, \
numbers and the symbols @/./+/-/_."),
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        help_text=_("Your password must contain at least 3 characters.")
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        help_text=_("To confirm, please enter the password again.")
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )


class UpdateUserForm(RegisterUserForm):

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            username = self.cleaned_data['username']
        return username
