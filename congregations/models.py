from djongo import models
from django.utils.translation import ugettext_lazy as _
TAGS = [
    ('ministerial_servant', _("Ministerial Servant")),
    ('attendant', _("Attendant")),
    ('soundman', _('Soundman')),
    ('mic_passer', _('Mic Passer')),
    ('reader_w', _("Reader Watchtower")),
    ('reader_m', _("Reader Midweek")),
    ('prayer', _("Prayer")),
    ('elder', _("Elder")),
    ('student', _("Student")),
    ('stage', _("Stage"))
]


class Congregation(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=180, verbose_name=_("Name"))
    circuit = models.CharField(max_length=20, verbose_name=_("Circuit"))
    city = models.CharField(max_length=80, verbose_name=_("City"))
    state = models.CharField(max_length=2, verbose_name=_("State"))

    objects = models.DjongoManager()

    def __str__(self):
        return self.name


class Group(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=80, verbose_name=_("Name"))
    congregation = models.ForeignKey(Congregation, verbose_name=_("Congregation"), on_delete=models.CASCADE)

    objects = models.DjongoManager()

    def __str__(self):
        return self.name


class Publisher(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    full_name = models.CharField(max_length=180, verbose_name=_("Full Name"))
    address = models.CharField(max_length=200, verbose_name=_("Address"), null=True, blank=True)
    email = models.CharField(max_length=180, verbose_name=_("Email"), null=True, blank=True)
    phone = models.CharField(max_length=80, verbose_name=_("Phone"), null=True, blank=True)
    cellphone = models.CharField(max_length=80, verbose_name=_("Cellphone"), null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"))
    update_date = models.DateTimeField(auto_now=True, verbose_name=_("Update Date"))
    baptism_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Baptism Date"))
    gender = models.CharField(max_length=1, verbose_name=_("Gender"), choices=[('f', _("Female")), ('m', _('Male'))])
    congregation = models.ForeignKey(
        Congregation, verbose_name=_("Congregation"), on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, verbose_name=_("Group"), on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ListField(models.CharField(max_length=80, choices=TAGS))
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)

    objects = models.DjongoManager()

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ('full_name', )
