from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import UserLoginForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        flash_messages = messages.get_messages(request)
        return render(
            request,
            'index.html',
            context={'messages': flash_messages},
        )


class UserLoginView(LoginView):
    template_name = 'login.html'
    class_form = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, _("You are logged in"))
        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
