from django.shortcuts import render, redirect
from django.views import View
# from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
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

#    def get(self, request, *args, **kwargs):
#        form = UserLoginForm()
#        flash_messages = messages.get_messages(request)
#        return render(
#            request,
#            'login.html',
#            context={'form': form, 'messages': flash_messages},
#        )
#
#    def post(self, request, *args, **kwargs):
#        form = UserLoginForm(request.POST)
#        if form.is_valid():
#            form.save()
#            cd = form.cleaned_data
#            user = authenticate(username=cd['username'], password=cd['password'])
#            if user and user.is_active:
#                login(request, user)
#                messages.success(request, _("You are logged in"))
#                return redirect('home')
#        return render(
#            request,
#            'login.html',
#            context={'form': form},
#        )


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
