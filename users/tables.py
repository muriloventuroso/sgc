import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _
from users.models import UserProfile


class TableUsers(tables.Table):

    username = tables.Column(accessor='user.username', verbose_name=_("Username"))
    is_staff = tables.Column(accessor='user.is_staff', verbose_name=_("Is Staff"))
    alter = tables.TemplateColumn(template_name='actions_table_users.html', verbose_name=_('Alter'))

    class Meta(object):
        attrs = {"class": "table"}
        model = UserProfile
        fields = ('username', 'is_staff')
