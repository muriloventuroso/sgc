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
