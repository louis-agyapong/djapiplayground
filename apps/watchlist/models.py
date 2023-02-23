from django.db import models
from django.utils.translation import gettext_lazy as _


class Movie(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    description = models.TextField(_("Description"), blank=True, default="")
    active = models.BooleanField(_("Active"), default=True)

    def __str__(self) -> str:
        return self.name
