import string
from django import forms
from django.utils.translation import ugettext_lazy as _
from datetimewidget.widgets import DateWidget
from meetings.models import (
    Meeting, Designations, WeekendContent, MidweekContent, TreasuresContent, ApplyYourselfContent,
    LivingChristiansContent, MeetingAudience)
from congregations.models import Publisher, Congregation


class FormMeeting(forms.ModelForm):
    def __init__(self, user_profile, language, *args, **kwargs):
        super(FormMeeting, self).__init__(*args, **kwargs)
        if user_profile.user.is_staff:
            self.fields['congregation'].queryset = Congregation.objects.all()
        else:
            self.fields['congregation'].queryset = user_profile.congregations.all()
        self.fields['congregation'].widget.attrs['disabled'] = True
        self.fields['congregation'].required = False
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
        model = Meeting
        fields = ('date', 'congregation', 'type_meeting')


class FormSearchMeeting(forms.Form):
    def __init__(self, language, *args, **kwargs):
        super(FormSearchMeeting, self).__init__(*args, **kwargs)
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

    class Meta:
        model = WeekendContent
        fields = ('president', 'speaker', 'speaker_congregation', 'theme', 'reader')


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
        congregation = Congregation.objects.get(pk=congregation_id)
        self.fields['person_treasure'].queryset = Publisher.objects.filter(
            tags__in=['elder', 'ministerial_servant'], congregation_id=congregation_id)
        self.fields['person_reading'].queryset = Publisher.objects.filter(
            tags__in=['student'], gender='m', congregation_id=congregation_id)
        self.fields['room_treasure'].choices = [
            (x.upper(), x.upper()) for x in list(string.ascii_lowercase)[:congregation.n_rooms]]
        if self.instance and self.instance.room_treasure:
            if list(string.ascii_lowercase).index(self.instance.room_treasure.lower()) + 1 > congregation.n_rooms:
                self.fields["room_treasure"].choices.append((self.instance.room_treasure, self.instance.room_treasure))

    person_reading = forms.ModelChoiceField(
        label=_("Person Reading"), queryset=Publisher.objects.none(),
        required=False)
    reading = forms.ChoiceField(label=_("Reading"), choices=[(False, _("No")), (True, _("Yes"))], initial=0)

    class Meta:
        model = TreasuresContent
        fields = (
            'title_treasure', 'person_treasure', 'person_reading', 'duration_treasure', 'reading', 'room_treasure')


class FormApplyYourselfContent(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormApplyYourselfContent, self).__init__(*args, **kwargs)
        congregation = Congregation.objects.get(pk=congregation_id)
        self.fields['student'].queryset = Publisher.objects.filter(
            tags__in=['student'], congregation_id=congregation_id)
        self.fields['assistant'].queryset = Publisher.objects.filter(
            tags__in=['student'], congregation_id=congregation_id)
        self.fields['room_apply'].choices = [
            (x.upper(), x.upper()) for x in list(string.ascii_lowercase)[:congregation.n_rooms]]
        if self.instance and self.instance.room_apply:
            if list(string.ascii_lowercase).index(self.instance.room_apply.lower()) + 1 > congregation.n_rooms:
                self.fields["room_apply"].choices.append((self.instance.room_apply, self.instance.room_apply))

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
        self.fields['attendant1'].queryset = Publisher.objects.filter(
            tags__in=['attendant'], congregation_id=congregation_id)
        self.fields['attendant2'].queryset = Publisher.objects.filter(
            tags__in=['attendant'], congregation_id=congregation_id)
        self.fields['mic_passer1'].queryset = Publisher.objects.filter(
            tags__in=['mic_passer'], congregation_id=congregation_id)
        self.fields['mic_passer2'].queryset = Publisher.objects.filter(
            tags__in=['mic_passer'], congregation_id=congregation_id)

    class Meta:
        model = Designations
        fields = ('soundman', 'attendant1', 'attendant2', 'mic_passer1', 'mic_passer2')


class FormGeneratePDF(forms.Form):
    def __init__(self, language, *args, **kwargs):
        super(FormGeneratePDF, self).__init__(*args, **kwargs)
        if language == 'en':
            self.fields['start_date'].widget.options['format'] = "YYYY-MM-DD"
            self.fields['end_date'].widget.options['format'] = "YYYY-MM-DD"
        elif language == 'pt-br':
            self.fields['start_date'].widget.options['format'] = "DD/MM/YYYY"
            self.fields['end_date'].widget.options['format'] = "DD/MM/YYYY"
    type_pdf = forms.ChoiceField(
        label=_("Type PDF"), choices=[('', ''), ('w', _("Weekend")), ('m', _("Midweek")), ('d', _('Designations'))],
        initial='', required=True)
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


class FormSearchMeetingAudience(forms.Form):
    def __init__(self, language, *args, **kwargs):
        super(FormSearchMeetingAudience, self).__init__(*args, **kwargs)
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


class FormMeetingAudience(forms.ModelForm):
    def __init__(self, language, *args, **kwargs):
        super(FormMeetingAudience, self).__init__(*args, **kwargs)

        if language == 'en':
            self.fields['date'].widget.options['format'] = "YYYY-MM-DD"
            if self.instance:
                kwargs.update(initial={
                    # 'field': 'value'
                    'date': self.instance.date.strftime("%Y-%m-%d")
                })
        elif language == 'pt-br':
            self.fields['date'].widget.options['format'] = "DD/MM/YYYY"
            if self.instance and self.instance.date:
                kwargs.update(initial={
                    # 'field': 'value'
                    'date': self.instance.date.strftime("%d/%m/%Y")
                })
    date = forms.DateField(
        label=_("Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=DateWidget(
            attrs={'id': "date", 'data-format': "YYYY-MM-DD"},
            usel10n=True, bootstrap_version=4, options={'format': 'YYYY-MM-DD'}))

    class Meta:
        model = MeetingAudience
        fields = ('date', 'filled_by', 'count', 'other', )
