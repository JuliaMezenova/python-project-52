from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import UserLoginForm
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(View):
    def get(self, request, *args, **kwargs):
        flash_messages = messages.get_messages(request)
        return render(
            request,
            'index.html',
            context={'messages': flash_messages},
        )


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    class_form = UserLoginForm
    success_message = _("You are logged in")


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
