import string
from django import forms
from django.utils.translation import gettext_lazy as _
from meetings.models import (
    Meeting, Designations, WeekendContent, MidweekContent, TreasuresContent, ApplyYourselfContent,
    LivingChristiansContent, MeetingAudience, SpeakerOut, Speech)
from congregations.models import Publisher, Congregation
from bson.objectid import ObjectId


class FormMeeting(forms.ModelForm):

    date = forms.DateField(
        label=_("Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))

    class Meta:
        model = Meeting
        fields = ('date', 'type_meeting')


class FormSearchMeeting(forms.Form):

    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))
    type_meeting = forms.ChoiceField(
        label=_("Type Meeting"), choices=[('', ''), ('w', _("Weekend")), ('m', _("Midweek"))],
        initial='', required=False)


class FormWeekendContent(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormWeekendContent, self).__init__(*args, **kwargs)
        self.fields['president'].queryset = Publisher.objects.filter(
            tags__in=['ministerial_servant', 'elder'], congregation_id=congregation_id)
        self.fields['reader'].queryset = Publisher.objects.filter(
            tags__in=['reader_w'], congregation_id=congregation_id)
        self.fields['theme'].choices = [
            ('', '')] + [(x.theme, str(x)) for x in Speech.objects.all().order_by('number')]
    theme = forms.ChoiceField(label=_("Theme"), required=False)

    class Meta:
        model = WeekendContent
        fields = ('president', 'speaker',
                  'speaker_congregation', 'theme', 'reader')


class FormMidweekContent(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormMidweekContent, self).__init__(*args, **kwargs)
        self.fields['initial_prayer'].queryset = Publisher.objects.filter(
            tags__in=['prayer'], congregation_id=congregation_id)
        self.fields['president'].queryset = Publisher.objects.filter(
            tags__in=['elder'], congregation_id=congregation_id)
        self.fields['final_prayer'].queryset = Publisher.objects.filter(
            tags__in=['prayer'], congregation_id=congregation_id)

    class Meta:
        model = MidweekContent
        fields = (
            'reading_week', 'initial_song', 'initial_prayer', 'president', 'second_song', 'final_prayer', 'final_song')


class FormTreasuresContent(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormTreasuresContent, self).__init__(*args, **kwargs)
        congregation = Congregation.objects.get(pk=ObjectId(congregation_id))
        self.fields['person_treasure'].queryset = Publisher.objects.filter(
            tags__in=['elder', 'ministerial_servant'], congregation_id=congregation_id)
        self.fields['person_reading'].queryset = Publisher.objects.filter(
            tags__in=['student'], gender='m', congregation_id=congregation_id)
        self.fields['room_treasure'].choices = [
            (x.upper(), x.upper()) for x in list(string.ascii_lowercase)[:congregation.n_rooms]]
        if self.instance and self.instance.room_treasure:
            if list(string.ascii_lowercase).index(self.instance.room_treasure.lower()) + 1 > congregation.n_rooms:
                self.fields["room_treasure"].choices.append(
                    (self.instance.room_treasure, self.instance.room_treasure))

    person_reading = forms.ModelChoiceField(
        label=_("Person Reading"), queryset=Publisher.objects.none(),
        required=False)
    reading = forms.ChoiceField(label=_("Reading"), choices=[
                                (False, _("No")), (True, _("Yes"))], initial=0)

    class Meta:
        model = TreasuresContent
        fields = (
            'title_treasure', 'person_treasure', 'person_reading', 'duration_treasure', 'reading', 'room_treasure')


class FormApplyYourselfContent(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormApplyYourselfContent, self).__init__(*args, **kwargs)
        congregation = Congregation.objects.get(pk=ObjectId(congregation_id))
        self.fields['student'].queryset = Publisher.objects.filter(
            tags__in=['student'], congregation_id=congregation_id)
        self.fields['assistant'].queryset = Publisher.objects.filter(
            tags__in=['student'], congregation_id=congregation_id)
        self.fields['room_apply'].choices = [
            (x.upper(), x.upper()) for x in list(string.ascii_lowercase)[:congregation.n_rooms]]
        if self.instance and self.instance.room_apply:
            if list(string.ascii_lowercase).index(self.instance.room_apply.lower()) + 1 > congregation.n_rooms:
                self.fields["room_apply"].choices.append(
                    (self.instance.room_apply, self.instance.room_apply))

    class Meta:
        model = ApplyYourselfContent
        fields = (
            'title_apply', 'student', 'assistant', 'duration_apply', 'room_apply')


class FormLivingChristiansContent(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormLivingChristiansContent, self).__init__(*args, **kwargs)
        self.fields['person_living'].queryset = Publisher.objects.filter(
            tags__in=['elder', 'ministerial_servant'], congregation_id=congregation_id)
        self.fields['reader'].queryset = Publisher.objects.filter(
            tags__in=['reader_m'], congregation_id=congregation_id)

    class Meta:
        model = LivingChristiansContent
        fields = (
            'title_living', 'person_living', 'reader', 'duration_living')


class FormDesignations(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormDesignations, self).__init__(*args, **kwargs)
        self.fields['soundman'].queryset = Publisher.objects.filter(
            tags__in=['soundman'], congregation_id=congregation_id)
        self.fields['attendant'].queryset = Publisher.objects.filter(
            tags__in=['attendant'], congregation_id=congregation_id)
        self.fields['mic_passer'].queryset = Publisher.objects.filter(
            tags__in=['mic_passer'], congregation_id=congregation_id)

    attendant = forms.ModelChoiceField(
        label=_("Attendant"), queryset=Publisher.objects.none(),
        required=False)
    mic_passer = forms.ModelChoiceField(
        label=_("Mic Passer"), queryset=Publisher.objects.none(),
        required=False)

    class Meta:
        model = Designations
        fields = ('soundman', )


class FormGeneratePDF(forms.Form):

    type_pdf = forms.ChoiceField(
        label=_("Type PDF"), choices=[('', ''), ('w', _("Weekend")), ('m', _("Midweek")), ('d', _('Designations'))],
        initial='', required=True)
    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))


class FormSearchMeetingAudience(forms.Form):

    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))


class FormMeetingAudience(forms.ModelForm):

    date = forms.DateField(
        label=_("Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))

    class Meta:
        model = MeetingAudience
        fields = ('date', 'filled_by', 'count', 'other', )


class FormSearchSpeakerOut(forms.Form):

    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))


class FormSpeakerOut(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormSpeakerOut, self).__init__(*args, **kwargs)
        self.fields['speaker'].queryset = Publisher.objects.filter(
            tags__in=['ministerial_servant', 'elder'], congregation_id=congregation_id)

    date = forms.DateField(
        label=_("Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))

    class Meta:
        model = SpeakerOut
        fields = ('date', 'speaker', 'theme', 'congregation_dest', )
