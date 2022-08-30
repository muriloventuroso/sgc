import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from meetings.models import Meeting, MeetingAudience, SpeakerOut, CountSpeech


class TableMeetings(tables.Table):

    alter = tables.TemplateColumn(template_name='actions_table_meetings.html', verbose_name=_("Alter"))

    class Meta(object):
        attrs = {"class": "table"}
        model = Meeting
        fields = ('date', 'type_meeting')


class TableMeetingAudience(tables.Table):

    alter = tables.TemplateColumn(template_name='actions_table_meeting_audiences.html', verbose_name=_('Alter'))

    class Meta(object):
        attrs = {"class": "table"}
        model = MeetingAudience
        fields = ('date', 'count')


class TableSpeakerOut(tables.Table):

    alter = tables.TemplateColumn(template_name='actions_table_speakers_out.html', verbose_name=_('Alter'))

    class Meta(object):
        attrs = {"class": "table"}
        model = SpeakerOut
        fields = ('date', 'speaker', 'congregation_dest')


class TableCountSpeech(tables.Table):

    class Meta(object):
        attrs = {"class": "table"}
        model = CountSpeech
        fields = ('speech', )
