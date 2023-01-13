from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Poll(models.Model):
    question = models.CharField(_("Question"), max_length=100)
    created_by = models.ForeignKey(User, verbose_name=_("Created By"), on_delete=models.CASCADE)
    pub_date = models.DateTimeField(_("Published Date"), auto_now=True)

    def __str__(self) -> str:
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey("Poll", verbose_name=_("Poll"), on_delete=models.CASCADE, related_name="polls")
    choice_text = models.CharField(_("Choice Text"), max_length=100)
    votes = models.IntegerField(_("Votes"), default=0)

    def __str__(self) -> str:
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey("Choice", verbose_name=_("Choice"), on_delete=models.CASCADE)
    poll = models.ForeignKey("Poll", verbose_name=_("Poll"), on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, verbose_name=_("Voted By"), on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(name="unique_poll_voted_by", fields=["poll", "voted_by"]),
        ]
