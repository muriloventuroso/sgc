from django import forms
from django.utils.translation import ugettext_lazy as _
from datetimewidget.widgets import DateWidget
from financial.models import Transaction


class FormTransaction(forms.ModelForm):
    def __init__(self, language, *args, **kwargs):
        super(FormTransaction, self).__init__(*args, **kwargs)
        if language == 'en':
            self.fields['date'].widget.options['format'] = "YYYY-MM-DD"
        elif language == 'pt-br':
            self.fields['date'].widget.options['format'] = "DD/MM/YYYY"
    date = forms.DateField(
        label=_("Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=DateWidget(
            attrs={'id': "date", 'data-format': "YYYY-MM-DD"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM-DD'}))

    class Meta:
        model = Transaction
        exclude = ('_id', 'congregation', 'user')


class FormSearchTransaction(forms.Form):
    def __init__(self, language, *args, **kwargs):
        super(FormSearchTransaction, self).__init__(*args, **kwargs)
        if language == 'en':
            self.fields['start_date'].widget.options['format'] = "YYYY-MM-DD"
            self.fields['end_date'].widget.options['format'] = "YYYY-MM-DD"
        elif language == 'pt-br':
            self.fields['start_date'].widget.options['format'] = "DD/MM/YYYY"
            self.fields['end_date'].widget.options['format'] = "DD/MM/YYYY"
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


class FormGeneratePDF(forms.Form):
    def __init__(self, language, *args, **kwargs):
        super(FormGeneratePDF, self).__init__(*args, **kwargs)
        if language == 'en':
            self.fields['month'].widget.options['format'] = "YYYY-MM"
        elif language == 'pt-br':
            self.fields['month'].widget.options['format'] = "MM/YYYY"
    type_pdf = forms.ChoiceField(
        label=_("Type PDF"), choices=[('', ''), ('s26', _("Transaction Sheet"))],
        initial='', required=True)
    month = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=DateWidget(
            attrs={'id': "start_date", 'data-format': "YYYY-MM"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM'}))
    balance = forms.DecimalField(label=_("Balance"), required=False)
