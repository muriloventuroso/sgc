from django import forms
from django.utils.translation import ugettext_lazy as _
from datetimewidget.widgets import DateWidget
from preaching.models import Pioneer, FieldServiceReport, TAGS
from congregations.models import Publisher


class FormPioneer(forms.ModelForm):
    def __init__(self, congregation_id, language, *args, **kwargs):
        super(FormPioneer, self).__init__(*args, **kwargs)
        if language == 'en':
            self.fields['start_date'].widget.options['format'] = "YYYY-MM"
            self.fields['start_date'].widget.options['format'] = "YYYY-MM"
        elif language == 'pt-br':
            self.fields['start_date'].widget.options['format'] = "MM/YYYY"
            self.fields['end_date'].widget.options['format'] = "YYYY-MM"
        self.fields['publisher'].queryset = Publisher.objects.filter(congregation_id=congregation_id)
    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=DateWidget(
            attrs={'id': "start_date", 'data-format': "YYYY-MM"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=DateWidget(
            attrs={'id': "end_date", 'data-format': "YYYY-MM"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM'}))

    class Meta:
        model = Pioneer
        exclude = ('_id', 'congregation', )


class FormSearchPioneer(forms.Form):
    def __init__(self, language, *args, **kwargs):
        super(FormSearchPioneer, self).__init__(*args, **kwargs)
        if language == 'en':
            self.fields['start_date'].widget.options['format'] = "YYYY-MM"
            self.fields['end_date'].widget.options['format'] = "YYYY-MM"
        elif language == 'pt-br':
            self.fields['start_date'].widget.options['format'] = "MM/YYYY"
            self.fields['end_date'].widget.options['format'] = "MM/YYYY"
    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=DateWidget(
            attrs={'id': "start_date", 'data-format': "YYYY-MM"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=DateWidget(
            attrs={'id': "end_date", 'data-format': "YYYY-MM"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM'}))


class FormFieldServiceReport(forms.ModelForm):
    def __init__(self, congregation_id, language, *args, **kwargs):
        super(FormFieldServiceReport, self).__init__(*args, **kwargs)
        if language == 'en':
            self.fields['date'].widget.options['format'] = "YYYY-MM"
            if hasattr(self.instance, 'pk') and self.instance.pk:
                self.initial['date'] = self.instance.date.strftime('%Y-%m')

        elif language == 'pt-br':
            self.fields['date'].widget.options['format'] = "MM/YYYY"
            if hasattr(self.instance, 'pk') and self.instance.pk:
                self.initial['date'] = self.instance.date.strftime('%m/%Y')

        self.fields['publisher'].queryset = Publisher.objects.filter(congregation_id=congregation_id)
    date = forms.DateField(
        label=_("Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=DateWidget(
            attrs={'id': "date", 'data-format': "YYYY-MM"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM'}))
    tags = forms.MultipleChoiceField(label=_("Tags"), choices=TAGS, required=False)

    class Meta:
        model = FieldServiceReport
        exclude = ('_id', 'congregation', )


class FormSearchFieldServiceReport(forms.Form):
    def __init__(self, congregation_id, language, *args, **kwargs):
        super(FormSearchFieldServiceReport, self).__init__(*args, **kwargs)
        if language == 'en':
            self.fields['start_date'].widget.options['format'] = "YYYY-MM"
            self.fields['end_date'].widget.options['format'] = "YYYY-MM"
        elif language == 'pt-br':
            self.fields['start_date'].widget.options['format'] = "MM/YYYY"
            self.fields['end_date'].widget.options['format'] = "MM/YYYY"
        self.fields['publisher'].queryset = Publisher.objects.filter(congregation_id=congregation_id)
    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=DateWidget(
            attrs={'id': "start_date", 'data-format': "YYYY-MM"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=DateWidget(
            attrs={'id': "end_date", 'data-format': "YYYY-MM"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM'}))
    publisher = forms.ModelChoiceField(label=_("Publisher"), queryset=Publisher.objects.none(), required=False)

