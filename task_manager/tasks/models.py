from django.db import models
from django.utils.translation import gettext as _
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    description = models.TextField(_('Description'), blank=True)
    status = models.ForeignKey(
        Status,
        verbose_name=_('Status'),
        on_delete=models.PROTECT
    )

    author = models.ForeignKey(
        User,
        verbose_name=_('Author'),
        on_delete=models.PROTECT,
        related_name='author'
    )

    executor = models.ForeignKey(
        User,
        verbose_name=_('Executor'),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='executor'
    )

    labels = models.CharField(_('Labels'), max_length=255, blank=True)
    created_at = models.DateTimeField(_('Date of creation'), auto_now_add=True)

    def __str__(self):
        return self.name
