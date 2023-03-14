from django import forms
from django.utils.translation import gettext_lazy as _
from congregations.models import Congregation, Group, Publisher, TAGS, CongregationRole, ROLES


class FormCongregation(forms.ModelForm):
    class Meta:
        model = Congregation
        fields = ('name', 'number', 'circuit', 'city', 'state',
                  'n_rooms', 'n_attendants', 'n_mic_passers', 'enable_board', 'theocratic_agenda')


class FormSearchCongregation(forms.Form):
    name = forms.CharField(label=_("Name"), required=False)
    circuit = forms.CharField(label=_("Circuit"), required=False)
    city = forms.CharField(label=_("City"), required=False)
    state = forms.CharField(label=_("State"), required=False)


class FormGroup(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormGroup, self).__init__(*args, **kwargs)
        if hasattr(self.instance, '_id') and self.instance._id:
            self.fields['leader'].queryset = Publisher.objects.filter(
                congregation_id=self.instance.congregation_id, gender="m", tags__in=['elder', 'ministerial_servant'])
            self.fields['assistant'].queryset = Publisher.objects.filter(
                congregation_id=self.instance.congregation_id, gender="m", tags__in=['elder', 'ministerial_servant'])
        else:
            del self.fields['leader']
            del self.fields['assistant']
        
    class Meta:
        model = Group
        fields = ('name', 'leader', 'assistant')


class FormSearchGroup(forms.Form):
    name = forms.CharField(label=_("Name"), required=False)


class FormPublisher(forms.ModelForm):
    def __init__(self, is_staff, congregation_id, *args, **kwargs):
        super(FormPublisher, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(
            congregation_id=congregation_id)
        if not is_staff:
            del self.fields['congregation']
    tags = forms.MultipleChoiceField(
        label=_("Tags"), choices=TAGS, required=False)
    baptism_date = forms.DateField(
        label=_("Baptism Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))

    class Meta:
        model = Publisher
        exclude = ('_id', 'creation_date', 'update_date')


class FormSearchPublisher(forms.Form):
    name = forms.CharField(label=_("Name"), required=False)
    tags = forms.MultipleChoiceField(
        label=_("TAGS"), choices=TAGS, required=False)
    group = forms.CharField(label=_("Group"), required=False)


class FormCongregationRole(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormCongregationRole, self).__init__(*args, **kwargs)
        self.fields['publisher'].queryset = Publisher.objects.filter(
            congregation_id=congregation_id, gender="m")

    class Meta:
        model = CongregationRole
        fields = ('role', 'publisher')


class FormSearchCongregationRole(forms.Form):
    role = forms.MultipleChoiceField(
        label=_("Role"), choices=ROLES, required=False)
