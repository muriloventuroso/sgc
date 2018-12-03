from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap_datepicker.widgets import DatePicker
from meetings.models import (
    Meeting, Designations, WeekendContent, MidweekContent, TreasuresContent, ApplyYourselfContent,
    LivingChristiansContent)
from congregations.models import Publisher


class FormMeeting(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%d/%m/%Y'], required=True, label=_('Date'),
        widget=DatePicker(options={"format": "dd/mm/yyyy"}, format="dd/mm/yyyy", fontawesome=True))

    class Meta:
        model = Meeting
        fields = ('date', 'congregation', 'type_meeting')


class FormSearchMeeting(forms.Form):
    start_date = forms.DateField(
        input_formats=['%d/%m/%Y'], required=False, label=_('Start Date'),
        widget=DatePicker(options={"format": "dd/mm/yyyy"}, format="dd/mm/yyyy", fontawesome=True))
    end_date = forms.DateField(
        input_formats=['%d/%m/%Y'], required=False, label=_('End Date'),
        widget=DatePicker(options={"format": "dd/mm/yyyy"}, format="dd/mm/yyyy", fontawesome=True))
    type_meeting = forms.ChoiceField(
        label=_("Type Meeting"), choices=[('', ''), ('w', _("Weekend")), ('m', _("Midweek"))],
        initial='', required=False)


class FormWeekendContent(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormWeekendContent, self).__init__(*args, **kwargs)
        self.fields['president'].queryset = Publisher.objects.filter(tags__in=['ministerial_servant', 'elder'])
        self.fields['reader'].queryset = Publisher.objects.filter(tags__in=['reader_w'])

    class Meta:
        model = WeekendContent
        fields = ('president', 'speaker', 'speaker_congregation', 'theme', 'reader')


class FormMidweekContent(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormMidweekContent, self).__init__(*args, **kwargs)
        self.fields['initial_prayer'].queryset = Publisher.objects.filter(tags__in=['prayer'])
        self.fields['president'].queryset = Publisher.objects.filter(tags__in=['elder'])
        self.fields['final_prayer'].queryset = Publisher.objects.filter(tags__in=['prayer'])

    class Meta:
        model = MidweekContent
        fields = (
            'reading_week', 'initial_song', 'initial_prayer', 'president', 'second_song', 'final_prayer', 'final_song')


class FormTreasuresContent(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormTreasuresContent, self).__init__(*args, **kwargs)
        self.fields['person_treasure'].queryset = Publisher.objects.filter(tags__in=['elder', 'ministerial_servant'])

    person_reading = forms.ModelChoiceField(
        label=_("Person Reading"), queryset=Publisher.objects.filter(tags__in=['student']).filter(gender='m'),
        required=False)
    reading = forms.ChoiceField(label=_("Reading"), choices=[(False, _("No")), (True, _("Yes"))], initial=0)

    class Meta:
        model = TreasuresContent
        fields = (
            'title_treasure', 'person_treasure', 'person_reading', 'duration_treasure', 'reading', 'room_treasure')


class FormApplyYourselfContent(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormApplyYourselfContent, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = Publisher.objects.filter(tags__in=['student'])
        self.fields['assistant'].queryset = Publisher.objects.filter(tags__in=['student'])

    class Meta:
        model = ApplyYourselfContent
        fields = (
            'title_apply', 'student', 'assistant', 'duration_apply', 'room_apply')


class FormLivingChristiansContent(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormLivingChristiansContent, self).__init__(*args, **kwargs)
        self.fields['person_living'].queryset = Publisher.objects.filter(tags__in=['elder', 'ministerial_servant'])
        self.fields['reader'].queryset = Publisher.objects.filter(tags__in=['reader_m'])

    class Meta:
        model = LivingChristiansContent
        fields = (
            'title_living', 'person_living', 'reader', 'duration_living')


class FormDesignations(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormDesignations, self).__init__(*args, **kwargs)
        self.fields['soundman'].queryset = Publisher.objects.filter(tags__in=['soundman'])
        self.fields['attendant1'].queryset = Publisher.objects.filter(tags__in=['attendant'])
        self.fields['attendant2'].queryset = Publisher.objects.filter(tags__in=['attendant'])
        self.fields['mic_passer1'].queryset = Publisher.objects.filter(tags__in=['mic_passer'])
        self.fields['mic_passer2'].queryset = Publisher.objects.filter(tags__in=['mic_passer'])

    class Meta:
        model = Designations
        fields = ('soundman', 'attendant1', 'attendant2', 'mic_passer1', 'mic_passer2')


class FormGeneratePDF(forms.Form):
    type_pdf = forms.ChoiceField(
        label=_("Type PDF"), choices=[('', ''), ('w', _("Weekend")), ('m', _("Midweek")), ('d', _('Designations'))],
        initial='', required=True)
    start_date = forms.DateField(
        input_formats=['%d/%m/%Y'], required=True, label=_('Start Date'),
        widget=DatePicker(options={"format": "dd/mm/yyyy"}, format="dd/mm/yyyy", fontawesome=True))
    end_date = forms.DateField(
        input_formats=['%d/%m/%Y'], required=True, label=_('End Date'),
        widget=DatePicker(options={"format": "dd/mm/yyyy"}, format="dd/mm/yyyy", fontawesome=True))
