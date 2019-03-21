import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _
from preaching.models import Pioneer


class TablePioneers(tables.Table):

    alter = tables.TemplateColumn(template_name='preaching/actions_table_pioneers.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = Pioneer
        fields = ('publisher', 'tp', 'start_date', 'is_active')
