from django.shortcuts import render, redirect
from django.views import View
from .models import Status
from .forms import StatusForm
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError


class IndexView(View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        flash_messages = messages.get_messages(request)
        return render(
            request,
            'statuses/index.html',
            context={
                'statuses': statuses,
                'messages': flash_messages,
            }
        )


class StatusFormCreateView(CreateView):
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _("Status successfully created"))
        return super().dispatch(request, *args, **kwargs)


class StatusFormUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully changed')


class StatusFormDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully deleted')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("The status cannot be deleted because it is in use."))
            return redirect(reverse_lazy('statuses_index'))
