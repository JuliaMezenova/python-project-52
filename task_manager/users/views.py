from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import User
from .forms import RegisterUserForm, UpdateUserForm
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError


class IndexView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()[:]
        flash_messages = messages.get_messages(request)
        return render(
            request,
            'users/index.html',
            context={
                'users': users,
                'messages': flash_messages,
            }
        )


class UserFormCreateView(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _("The user has been successfully registered")


class UserFormUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_index')
    success_message = _("The user has been successfully changed")

    def get(self, request, *args, **kwargs):
        url_id = kwargs.get('pk')
        current_user_id = self.request.user.id
        if url_id != current_user_id:
            messages.error(request, _("You do not have the rights to change another user."))
            return redirect(reverse_lazy('users_index'))
        return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You are not logged in! Please log in."))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        password = form.cleaned_data.get('password1')
        if password:
            self.object.set_password(password)
        return super().form_valid(form)


class UserFormDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')
    success_message = _("The user has been successfully deleted")

    def get(self, request, *args, **kwargs):
        current_user_id = self.request.user.id
        url_id = kwargs.get('pk')
        if url_id != current_user_id:
            messages.error(request, _("You do not have the rights to change another user."))
            return redirect(reverse_lazy('users_index'))
        return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You are not logged in! Please log in."))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                _("It is not possible to delete a user because it is being used")
            )
            return redirect(reverse_lazy('users_index'))
