from djongo import models
from django.contrib.auth.models import User
from congregations.models import Congregation


class UserProfile(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(User, models.CASCADE)
    congregations = models.ManyToManyField(Congregation)

    objects = models.DjongoManager()

    def __str__(self):
        return self.user.username
