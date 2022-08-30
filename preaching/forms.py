from django import forms
from django.utils.translation import gettext_lazy as _
from preaching.models import Pioneer, FieldServiceReport, TAGS
from congregations.models import Publisher


class FormPioneer(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormPioneer, self).__init__(*args, **kwargs)

        self.fields['publisher'].queryset = Publisher.objects.filter(
            congregation_id=congregation_id)
    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'month-field'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'month-field'}))

    class Meta:
        model = Pioneer
        exclude = ('_id', 'congregation', )


class FormSearchPioneer(forms.Form):
    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'month-field'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'month-field'}))


class FormFieldServiceReport(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormFieldServiceReport, self).__init__(*args, **kwargs)

        self.fields['publisher'].queryset = Publisher.objects.filter(
            congregation_id=congregation_id)
    date = forms.DateField(
        label=_("Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'month-field'}))
    tags = forms.MultipleChoiceField(
        label=_("Tags"), choices=TAGS, required=False)

    class Meta:
        model = FieldServiceReport
        exclude = ('_id', 'congregation')


class FormSearchFieldServiceReport(forms.Form):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormSearchFieldServiceReport, self).__init__(*args, **kwargs)

        self.fields['publisher'].queryset = Publisher.objects.filter(
            congregation_id=congregation_id)
    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'month-field'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'month-field'}))
    publisher = forms.ModelChoiceField(
        label=_("Publisher"), queryset=Publisher.objects.none(), required=False)
