from django.db import models
from django.utils.translation import gettext as _


class Status(models.Model):
    name = models.CharField(_("Status"), max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
