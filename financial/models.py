from djongo import models
from django.utils.translation import ugettext_lazy as _
from congregations.models import Congregation
from django.contrib.auth.models import User
TRANSACTION_CODE = [
    ('C', _("Congregation")),
    ('O', _("World Wide Work")),
    ('D', _("Expense"))
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


class TransactionCategory(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE, verbose_name=_("Congregation"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("User"))

    objects = models.DjongoManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Transaction Category")
        verbose_name_plural = _("Transaction Categories")


class Transaction(models.Model):
    _id = models.ObjectIdField()
    date = models.DateField(verbose_name=_("Date"))
    description = models.TextField(verbose_name=_("Description"))
    tc = models.CharField(max_length=1, verbose_name=_("Transaction Code"), choices=TRANSACTION_CODE, blank=True)
    tt = models.CharField(max_length=1, verbose_name=_("Transaction Type"), choices=TRANSACTION_TYPE)
    td = models.CharField(max_length=1, verbose_name=_("Transaction Direction"), choices=TRANSACTION_DIRECTION)
    value = models.DecimalField(verbose_name=_("Value"), default=0, decimal_places=2, max_digits=10)
    note = models.TextField(verbose_name=_("Note"), blank=True)
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE, verbose_name=_("Congregation"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("User"))
    category = models.ForeignKey(
        TransactionCategory, on_delete=models.PROTECT, verbose_name=_("Category"), null=True, blank=True)

    objects = models.DjongoManager()

    def __str__(self):
        return '({}) - {}'.format(self.date, self.description)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")



