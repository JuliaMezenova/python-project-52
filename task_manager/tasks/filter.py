from django import forms
import django_filters
from .models import Task
from ..labels.models import Label
from django.utils.translation import gettext as _


class TaskFilter(django_filters.FilterSet):
    label = django_filters.ModelChoiceFilter(
        label=_("Label"),
        field_name='labels',
        queryset=Label.objects.all()
    )
    only_self_tasks = django_filters.BooleanFilter(
        label=_('Only self tasks'),
        widget=forms.CheckboxInput,
        method='filter_created_by_author'
    )

    def filter_created_by_author(self, queryset, author, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'only_self_tasks']
