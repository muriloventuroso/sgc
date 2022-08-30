import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from preaching.models import Pioneer, FieldServiceReport


class TablePioneers(tables.Table):

    alter = tables.TemplateColumn(template_name='actions_table_pioneers.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = Pioneer
        fields = ('publisher', 'tp', 'start_date', 'is_active')


class TableFieldServiceReports(tables.Table):

    alter = tables.TemplateColumn(
        template_name='actions_table_field_service_reports.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = FieldServiceReport
        fields = ('publisher', 'date', 'hours', 'placements', 'return_visits')
