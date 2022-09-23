from djongo import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from congregations.models import Congregation, Publisher


class User(AbstractBaseUser):
    _id = models.ObjectIdField(primary_key=True)
    congregation = models.ForeignKey(
        Congregation, verbose_name=_("Congregation"), null=True, blank=True, on_delete=models.SET_NULL)
    publisher = models.ForeignKey(
        Publisher, verbose_name=_("Publisher"), null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(
        _('first name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(
        _('last name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    phone = models.CharField(max_length=80, null=True,
                             blank=True, verbose_name=_('Phone Number'))
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. \
        Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    objects = models.DjongoManager()

    USERNAME_FIELD = 'email'

    objects = models.DjongoManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email']

    @property
    def username(self):
        return self.email
