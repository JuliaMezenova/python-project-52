from django.shortcuts import render, redirect
from django.views import View
from .models import Label
from .forms import LabelForm
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError


class IndexView(View):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        flash_messages = messages.get_messages(request)
        return render(
            request,
            'labels/index.html',
            context={
                'labels': labels,
                'messages': flash_messages,
            }
        )


class LabelFormCreateView(SuccessMessageMixin, CreateView):
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels_index')
    success_message = _("Label successfully created")


class LabelFormUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('Label successfully changed')


class LabelFormDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('Label successfully deleted')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                _("It is not possible to delete a label because it is being used")
            )
            return redirect(reverse_lazy('labels_index'))
