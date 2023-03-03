from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class StreamingPlatform(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    about = models.TextField(_("About"), blank=True, default="")
    website = models.URLField(_("Website URL"), max_length=100, blank=True, default="")

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    title = models.CharField(_("Name"), max_length=50)
    description = models.TextField(_("Description"), blank=True, default="")
    platform = models.ForeignKey(
        StreamingPlatform,
        verbose_name=_("Platform"),
        on_delete=models.SET_NULL,
        related_name="movies",
        blank=True,
        null=True,
    )
    active = models.BooleanField(_("Active"), default=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(
        Movie, verbose_name=_("Movie"), on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveIntegerField(
        _("Rating"), validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.TextField(_("Description"), blank=True, default="")
    created = models.DateTimeField(_("Create At"), auto_now_add=True)
    updated = models.DateTimeField(_("Updatd At"), auto_now=True)
    active = models.BooleanField(_("Active"), default=True)

    def __str__(self) -> str:
        return f"Movie: {self.movie.title} Rating: {str(self.rating)}" 
