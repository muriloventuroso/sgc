import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from users.models import User


class TableUsers(tables.Table):

    congregation = tables.TemplateColumn(
        '{{record.congregation}}', verbose_name=_("Congregation"))
    alter = tables.TemplateColumn(
        template_name='actions_table_users.html', verbose_name=_('Alter'))

    class Meta(object):
        attrs = {"class": "table"}
        model = User
        fields = ('email', 'is_staff')
