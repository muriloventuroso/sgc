import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from congregations.models import Congregation, Group, Publisher, CongregationRole


class TableCongregations(tables.Table):

    alter = tables.TemplateColumn(
        template_name='congregations/actions_table_congregations.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = Congregation
        fields = ('name', 'number', 'circuit', 'city', 'state')


class TableGroups(tables.Table):

    alter = tables.TemplateColumn(template_name='groups/actions_table_groups.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = Group
        fields = ('name', )


class TablePublishers(tables.Table):

    alter = tables.TemplateColumn(template_name='publishers/actions_table_publishers.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = Publisher
        fields = ('full_name', 'email', 'group')


class TableCongregationRoles(tables.Table):

    alter = tables.TemplateColumn(
        template_name='congregations/actions_table_congregation_roles.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = CongregationRole
        fields = ('role', 'publisher')
