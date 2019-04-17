import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _
from financial.models import Transaction, TransactionCategory


class TableTransactions(tables.Table):

    alter = tables.TemplateColumn(template_name='actions_table_transactions.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = Transaction
        fields = ('date', 'description', 'tc', 'td', 'tt', 'value')


class TableTransactionCategories(tables.Table):

    alter = tables.TemplateColumn(template_name='actions_table_transactioncategories.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = TransactionCategory
        fields = ('name', )
