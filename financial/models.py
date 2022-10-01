from djongo import models
from djongo.models import ObjectIdField
from django.db.models import DecimalField
from django.utils.translation import gettext_lazy as _
from congregations.models import Congregation
from users.models import User
TRANSACTION_CODE = [
    ('C', _("Congregation")),
    ('CE', _("Congregation (Electronic)")),
    ('O', _("World Wide Work")),
    ('D', _("Account Deposit")),
    ('G', _("Expense")),
    ('F', _("Construction of the Subsidiary")),
    ('J', _("Interest")),
    ('OE', _("Specific objective")),
    ('GP', _("Expense paid for by Bethel"))
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
    _id = ObjectIdField()
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    congregation = models.ForeignKey(
        Congregation, on_delete=models.CASCADE, verbose_name=_("Congregation"))
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("User"))

    objects = models.DjongoManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Transaction Category")
        verbose_name_plural = _("Transaction Categories")


class SubTransaction(models.Model):
    date = models.DateField(verbose_name=_("Date"), blank=True, null=True)
    description = models.TextField(
        verbose_name=_("Description"), help_text=_("Leave blank for a transaction on the same line as the main one"),
        blank=True)
    tc = models.CharField(max_length=2, verbose_name=_(
        "Transaction Code"), choices=TRANSACTION_CODE, blank=True)
    tt = models.CharField(max_length=1, verbose_name=_(
        "Transaction Type"), choices=TRANSACTION_TYPE)
    td = models.CharField(max_length=2, verbose_name=_(
        "Transaction Direction"), choices=TRANSACTION_DIRECTION)
    value = models.FloatField(verbose_name=_("Value"), default=0)
    category = models.ForeignKey(
        TransactionCategory, on_delete=models.PROTECT, verbose_name=_("Category"), null=True, blank=True)

    class Meta:
        abstract = True


class Transaction(models.Model):
    _id = ObjectIdField()
    date = models.DateField(verbose_name=_("Date"), blank=True)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    tc = models.CharField(max_length=2, verbose_name=_(
        "Transaction Code"), choices=TRANSACTION_CODE, blank=True)
    tt = models.CharField(max_length=1, verbose_name=_(
        "Transaction Type"), choices=TRANSACTION_TYPE)
    td = models.CharField(max_length=2, verbose_name=_(
        "Transaction Direction"), choices=TRANSACTION_DIRECTION)
    value = models.FloatField(verbose_name=_("Value"), default=0)
    note = models.TextField(verbose_name=_("Note"), blank=True)
    congregation = models.ForeignKey(
        Congregation, on_delete=models.CASCADE, verbose_name=_("Congregation"))
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("User"))
    category = models.ForeignKey(
        TransactionCategory, on_delete=models.PROTECT, verbose_name=_("Category"), null=True, blank=True)
    hide_from_sheet = models.BooleanField(verbose_name=_(
        "Hide from Transaction Sheet"), default=False)
    sub_transactions = models.ArrayModelField(model_container=SubTransaction)

    objects = models.DjongoManager()

    def __str__(self):
        return '({}) - {}'.format(self.date, self.description)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ['date', ]


class TransactionContent(models.Model):
    tc = models.CharField(max_length=2, verbose_name=_(
        "Transaction Code"), choices=TRANSACTION_CODE, blank=True)
    count = models.IntegerField(verbose_name=_("Count"))
    value = models.DecimalMongoField(verbose_name=_(
        "Value"), default=0, decimal_places=2, max_digits=10)


class MonthlySummary(models.Model):
    _id = ObjectIdField()
    date = models.DateField(verbose_name=_("Date"))
    carried_balance = DecimalField(verbose_name=_(
        "Carried Balance"), default=0, decimal_places=2, max_digits=10)
    final_balance = DecimalField(verbose_name=_(
        "Final Balance"), default=0, decimal_places=2, max_digits=10)
    transactions = models.ArrayModelField(model_container=TransactionContent)
    congregation = models.ForeignKey(
        Congregation, on_delete=models.CASCADE, verbose_name=_("Congregation"))

    objects = models.DjongoManager()

    class Meta:
        verbose_name = _("Monthly Summary")
        verbose_name_plural = _("Monthly Summaries")
        ordering = ['-date', ]
