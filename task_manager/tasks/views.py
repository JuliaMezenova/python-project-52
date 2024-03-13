from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Task
from .forms import TaskForm
from django.utils.translation import gettext as _
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()[:]
        flash_messages = messages.get_messages(request)
        return render(
            request,
            'tasks/index.html',
            context={
                'tasks': tasks,
                'messages': flash_messages,
            }
        )


class TaskFormCreateView(CreateView):
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _("Task successfully created"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class TaskFormUpdateView(SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully changed')


class TaskFormDeleteView(SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task deleted successfully')

    def get(self, request, *args, **kwargs):
        current_user_id = self.request.user.id
        url_id = kwargs.get('pk')
        task = Task.objects.get(pk=url_id)
        if task.author.id != current_user_id:
            messages.error(request, _('Only its author can delete a task'))
            return redirect(reverse_lazy('tasks_index'))
        return super().get(request, *args, **kwargs)


class TaskShowIndex(DetailView):
    model = Task
    template_name = 'tasks/task_show.html'
    context_object_name = 'task'
