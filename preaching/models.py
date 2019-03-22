from djongo import models
from django.utils.translation import ugettext_lazy as _
from congregations.models import Congregation, Publisher
TAGS = [
    ('auxiliary_pioneer', _("Auxiliary Pioneer")),
    ('regular_pioneer', _("Regular Pioneer"))
]
TYPES_PIONEER = [
    ('a', _("Auxiliary Pioneer")),
    ('r', _("Regular Pioneer"))
]


class FieldServiceReport(models.Model):
    _id = models.ObjectIdField()
    date = models.DateField(verbose_name=_("Date"))
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name=_("Publisher"))
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE, verbose_name=_("Congregation"))
    tags = models.ListField(models.CharField(max_length=80, choices=TAGS))
    hours = models.IntegerField(verbose_name=_("Hours"), default=0)
    placements = models.IntegerField(verbose_name=_("Placements"), default=0)
    video = models.IntegerField(verbose_name=_("Video Showings"), default=0)
    return_visits = models.IntegerField(verbose_name=_("Return Visits"), default=0)
    studies = models.IntegerField(verbose_name=_("Studies"), default=0)
    note = models.TextField(verbose_name=_("Note"), blank=True)

    objects = models.DjongoManager()

    def __str__(self):
        return '({}) - {}'.format(self.date, self.publisher)

    class Meta:
        verbose_name = _("Field Service Report")
        verbose_name_plural = _("Field Service Reports")


class Pioneer(models.Model):
    _id = models.ObjectIdField()
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"), null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name=_("Publisher"))
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE, verbose_name=_("Congregation"))
    tp = models.CharField(max_length=1, choices=TYPES_PIONEER, verbose_name=_("Type"))
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)

    objects = models.DjongoManager()

    def __str__(self):
        return '({}) - {}'.format(self.get_tp_display(), self.publisher)

    class Meta:
        verbose_name = _("Pioneer")
        verbose_name_plural = _("Pioneers")
