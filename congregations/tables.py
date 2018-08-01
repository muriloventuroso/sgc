import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _
from congregations.models import Congregation, Group, Publisher


class TableCongregations(tables.Table):

    def __init__(self, *args, **kwargs):
        super(TableCongregations, self).__init__(*args, **kwargs)
        self.base_columns['alter'].verbose_name = _('Alter')

    alter = tables.TemplateColumn(template_name='congregations/actions_table_congregations.html')

    class Meta(object):
        attrs = {"class": "table"}
        model = Congregation
        fields = ('name', 'circuit', 'city', 'state')


class TableGroups(tables.Table):

    def __init__(self, *args, **kwargs):
        super(TableGroups, self).__init__(*args, **kwargs)
        self.base_columns['alter'].verbose_name = _('Alter')

    alter = tables.TemplateColumn(template_name='groups/actions_table_groups.html')

    class Meta(object):
        attrs = {"class": "table"}
        model = Group
        fields = ('name', )


class TablePublishers(tables.Table):

    def __init__(self, *args, **kwargs):
        super(TablePublishers, self).__init__(*args, **kwargs)
        self.base_columns['alter'].verbose_name = _('Alter')

    alter = tables.TemplateColumn(template_name='publishers/actions_table_publishers.html')

    class Meta(object):
        attrs = {"class": "table"}
        model = Publisher
        fields = ('full_name', 'email')
