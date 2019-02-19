from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap_datepicker.widgets import DatePicker
from congregations.models import Congregation, Group, Publisher, TAGS


class FormCongregation(forms.ModelForm):
    class Meta:
        model = Congregation
        fields = ('name', 'circuit', 'city', 'state')


class FormSearchCongregation(forms.Form):
    name = forms.CharField(label=_("Name"), required=False)
    circuit = forms.CharField(label=_("Circuit"), required=False)
    city = forms.CharField(label=_("City"), required=False)
    state = forms.CharField(label=_("State"), required=False)


class FormGroup(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'congregation',)


class FormSearchGroup(forms.Form):
    name = forms.CharField(label=_("Name"), required=False)


class FormPublisher(forms.ModelForm):
    tags = forms.MultipleChoiceField(label=_("Tags"), choices=TAGS)
    baptism_date = forms.DateField(
        input_formats=['%d/%m/%Y'], required=False, label=_('Baptism Date'),
        widget=DatePicker(options={"format": "dd/mm/yyyy"}, format="dd/mm/yyyy", fontawesome=True))

    class Meta:
        model = Publisher
        exclude = ('_id', 'creation_date', 'update_date')


class FormSearchPublisher(forms.Form):
    def __init__(self, user_profile, *args, **kwargs):
        super(FormSearchPublisher, self).__init__(*args, **kwargs)
        if user_profile.user.is_staff:
            self.fields['congregation'].queryset = Congregation.objects.all()
        else:
            self.fields['congregation'].queryset = user_profile.congregations.all()
    name = forms.CharField(label=_("Name"), required=False)
    tags = forms.MultipleChoiceField(label=_("TAGS"), choices=TAGS, required=False)
    congregation = forms.ModelChoiceField(label=_("Congregation"), queryset=Congregation.objects.none(), required=False)
