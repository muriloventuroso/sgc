from django import forms
from django.utils.translation import ugettext_lazy as _
from datetimewidget.widgets import DateWidget
from financial.models import Transaction


class FormTransaction(forms.ModelForm):
    date = forms.DateField(
        label=_("Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=DateWidget(
            attrs={'id': "date", 'data-format': "YYYY-MM-DD"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM-DD'}))

    class Meta:
        model = Transaction
        exclude = ('_id', 'congregation', 'user')


class FormSearchTransaction(forms.Form):
    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=DateWidget(
            attrs={'id': "start_date", 'data-format': "YYYY-MM-DD"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM-DD'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=DateWidget(
            attrs={'id': "end_date", 'data-format': "YYYY-MM-DD"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM-DD'}))
