from django.db import models
from django.utils.translation import gettext as _


class Label(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
