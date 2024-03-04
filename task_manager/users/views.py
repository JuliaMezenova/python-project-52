from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import User
from .forms import RegisterUserForm
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()[:]
        flash_messages = messages.get_messages(request)
        return render(
            request,
            'users/index.html',
            context = {'users': users, 'messages': flash_messages}
        )



class UserFormCreateView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, _("The user has been successfully registered"))
        return super().dispatch(request, *args, **kwargs)

#    def get(self, request, *args, **kwargs):
#        form = UserForm()
#        return render(
#            request,
#            'users/create.html',
#            context={'form': form},
#        )
#
#    def post(self, request, *args, **kwargs):
#        form = UserForm(request.POST)
#        if form.is_valid():
#            form.save(commit=False)
#
#            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
#                return redirect(reverse('user_create'))
#            form.save()
#            messages.success(request, _("The user has been successfully registered"))
#            return redirect('login')
#        else:
#            return render(
#                request,
#                'users/create.html',
#                context={'form': form}
#            )


class UserFormUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = RegisterUserForm
    fields = '__all__'
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_index')
    success_message = _("The user has been successfully changed")
    
    def get(self, request, *args, **kwargs):
        url_id = kwargs.get('id')
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
        password = form.cleaned_data.get('password1')
        if password:
            self.object.set_password(password)
        return super().form_valid(form)

# def get(self, request, *args, **kwargs):
#        url_id = kwargs.get('id')
#        user = User.objects.get(id=url_id)
#        form = UserForm(instance=user)
#        changing_user_id = self.request.user.id
#        if url_id != changing_user_id:
#            messages.error(request, _("You do not have the rights to change another user."))
#            return redirect('users_index')
#        return render(
#            request,
#            'users/update.html',
#            context={'form': form, 'user_id': user_id},
#        )
#
#    def post(self, request, *args, **kwargs):
#        user_id = kwargs.get('id')
#        user = User.objects.get(id=user_id)
#        form = UserForm(request.POST, instance=user)
#        if form.is_valid():
#            form.save()
#            messages.success(request, _("The user has been successfully changed"))
#            return redirect('users_index')
#        return render(
#            request,
#            'users/update.html',
#            context={'form': form, 'user_id': user_id}
#        )


class UserFormDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')
    success_message = _("The user has been successfully deleted")

    def get_object(self, *args, **kwargs):
        user = self.request.user
        return user

    def get(self, request, *args, **kwargs):
        current_user_id = self.request.user.id
        url_id = kwargs.get('id')
        if url_id != current_user_id:
            messages.error(request, _("You do not have the rights to change another user."))
            return redirect(reverse_lazy('users_index'))
        return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You are not logged in! Please log in."))
        return super().dispatch(request, *args, **kwargs)
#    def post(self, request, *args, **kwargs):
#        return super().post(request, *args, **kwargs)
#        user_id = kwargs.get('id')
#        user = User.objects.get(id=user_id)
#        if user:
#            user.delete()
#            messages.success(request, _("The user has been successfully deleted"))
#        return redirect('users_index')
