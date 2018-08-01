import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _
from meetings.models import Meeting


class TableMeetings(tables.Table):

    def __init__(self, *args, **kwargs):
        super(TableMeetings, self).__init__(*args, **kwargs)
        self.base_columns['alter'].verbose_name = _('Alter')

    alter = tables.TemplateColumn(template_name='actions_table_meetings.html')

    class Meta(object):
        attrs = {"class": "table"}
        model = Meeting
        fields = ('date', 'type_meeting')
