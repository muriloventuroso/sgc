import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _
from financial.models import Transaction, TransactionCategory, MonthlySummary


class TableTransactions(tables.Table):

    alter = tables.TemplateColumn(template_name='actions_table_transactions.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = Transaction
        fields = ('date', 'description', 'tc', 'td', 'tt', 'category', 'value')


class TableTransactionCategories(tables.Table):

    alter = tables.TemplateColumn(template_name='actions_table_transactioncategories.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = TransactionCategory
        fields = ('name', )


class TableMonthlySummary(tables.Table):
    date = tables.Column(verbose_name=_("Month"))

    class Meta(object):
        attrs = {"class": "table"}
        model = MonthlySummary
        fields = ('date', 'carried_balance', 'final_balance')


class TableConfrontation(tables.Table):
    month = tables.Column(verbose_name=_("Month"))
    sum_receipts_in = tables.TemplateColumn('{{record.sum_receipts_in|floatformat:2}}', verbose_name=_("Receipts In"))
    sum_receipts_out = tables.TemplateColumn(
        '{{record.sum_receipts_out|floatformat:2}}', verbose_name=_("Receipts Out"))
    receipts_final_balance = tables.TemplateColumn(
        '{{record.receipts_final_balance|floatformat:2}}', verbose_name=_("Receipts Final Balance"))
    account_carried_balance = tables.TemplateColumn(
        '{{record.account_carried_balance|floatformat:2}}', verbose_name=_("Checking Account Carried Balance"))
    sum_account_in = tables.TemplateColumn(
        '{{record.sum_account_in|floatformat:2}}', verbose_name=_("Checking Account In"))
    sum_account_out = tables.TemplateColumn(
        '{{record.sum_account_out|floatformat:2}}', verbose_name=_("Checking Account Out"))
    account_final_balance = tables.TemplateColumn(
        '{{record.account_final_balance|floatformat:2}}', verbose_name=_("Checking Account Final Balance"))
