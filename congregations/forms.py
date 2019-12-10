from django import forms
from django.utils.translation import ugettext_lazy as _
from datetimewidget.widgets import DateWidget
from congregations.models import Congregation, Group, Publisher, TAGS, CongregationRole, ROLES


class FormCongregation(forms.ModelForm):
    class Meta:
        model = Congregation
        fields = ('name', 'circuit', 'city', 'state', 'n_rooms', 'n_attendants', 'n_mic_passers')


class FormSearchCongregation(forms.Form):
    name = forms.CharField(label=_("Name"), required=False)
    circuit = forms.CharField(label=_("Circuit"), required=False)
    city = forms.CharField(label=_("City"), required=False)
    state = forms.CharField(label=_("State"), required=False)


class FormGroup(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', )


class FormSearchGroup(forms.Form):
    name = forms.CharField(label=_("Name"), required=False)


class FormPublisher(forms.ModelForm):
    def __init__(self, congregation_id, *args, **kwargs):
        super(FormPublisher, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(congregation_id=congregation_id)
    tags = forms.MultipleChoiceField(label=_("Tags"), choices=TAGS)
    baptism_date = forms.DateField(
        label=_("Baptism Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=DateWidget(
            attrs={'id': "start_date", 'data-format': "YYYY-MM-DD"},
            usel10n=False, bootstrap_version=4, options={'format': 'YYYY-MM-DD'}))

    class Meta:
        model = Publisher
        exclude = ('_id', 'creation_date', 'update_date', 'congregation')


class FormSearchPublisher(forms.Form):
    name = forms.CharField(label=_("Name"), required=False)
    tags = forms.MultipleChoiceField(label=_("TAGS"), choices=TAGS, required=False)
    group = forms.CharField(label=_("Group"), required=False)


class FormCongregationRole(forms.ModelForm):
    class Meta:
        model = CongregationRole
        fields = ('role', 'publisher')


class FormSearchCongregationRole(forms.Form):
    publisher = forms.CharField(label=_("Publisher"), required=False)
    role = forms.MultipleChoiceField(label=_("Role"), choices=ROLES, required=False)
