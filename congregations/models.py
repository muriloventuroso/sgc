from djongo import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
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
ROLES = [
    ('account_servant', _("Account Servant")),
    ('secretary', _("Secretary")),
    ('coordinator', _("Coordinator")),
    ('ss', _("Superintendent of Service"))
]


class Congregation(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=180, verbose_name=_("Name"))
    circuit = models.CharField(max_length=20, verbose_name=_("Circuit"))
    city = models.CharField(max_length=80, verbose_name=_("City"))
    state = models.CharField(max_length=2, verbose_name=_("State"))
    n_rooms = models.IntegerField(default=1, verbose_name=_("Number of Rooms"), validators=[
        MaxValueValidator(2),
        MinValueValidator(1)
    ])

    objects = models.DjongoManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Congregation")
        verbose_name_plural = _("Congregations")


class Group(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=80, verbose_name=_("Name"))
    congregation = models.ForeignKey(Congregation, verbose_name=_("Congregation"), on_delete=models.CASCADE)

    objects = models.DjongoManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


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
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")


class CongregationRole(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    congregation = models.ForeignKey(Congregation, verbose_name=_("Congregation"), on_delete=models.CASCADE)
    role = models.CharField(max_length=80, choices=ROLES, verbose_name=_("Role"))
    publisher = models.ForeignKey(Publisher, verbose_name=_("Publisher"), on_delete=models.CASCADE)

    objects = models.DjongoManager()
