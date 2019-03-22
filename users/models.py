from djongo import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from congregations.models import Congregation


class UserProfile(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(User, models.CASCADE)
    congregation = models.ForeignKey(
        Congregation, verbose_name=_("Congregation"), null=True, blank=True, on_delete=models.SET_NULL)

    objects = models.DjongoManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
