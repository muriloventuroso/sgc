from djongo import models
from django.utils.translation import ugettext_lazy as _
from congregations.models import Congregation
from django.contrib.auth.models import User
TRANSACTION_CODE = [
    ('C', _("Congregation")),
    ('O', _("World Wide Work")),
    ('D', _("Bank Account Deposit")),
    ('S', _("World Kingdom Hall Construction"))
]
TRANSACTION_TYPE = [
    ('R', _("Receips")),
    ('C', _("Checking Account")),
    ('O', _("Other"))
]
TRANSACTION_DIRECTION = [
    ('I', _("In")),
    ('O', _("Out"))
]


class Transaction(models.Model):
    _id = models.ObjectIdField()
    date = models.DateField(verbose_name=_("Date"))
    description = models.TextField(verbose_name=_("Description"))
    tc = models.CharField(max_length=1, verbose_name=_("Transaction Code"), choices=TRANSACTION_CODE)
    tt = models.CharField(max_length=1, verbose_name=_("Transaction Type"), choices=TRANSACTION_TYPE)
    td = models.CharField(max_length=1, verbose_name=_("Transaction Direction"), choices=TRANSACTION_DIRECTION)
    note = models.TextField(verbose_name=_("Note"), blank=True)
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE, verbose_name=_("Congregation"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("User"))

    objects = models.DjongoManager()

    def __str__(self):
        return '({}) - {}'.format(self.date, self.description)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
