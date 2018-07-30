from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap_datepicker.widgets import DatePicker
from congregations.models import Congregation, Group, Publisher, TAGS


class FormCongregation(forms.ModelForm):
    class Meta:
        model = Congregation
        fields = ('name', 'circuit', 'city', 'state')


class FormGroup(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'congregation',)


class FormPublisher(forms.ModelForm):
    tags = forms.MultipleChoiceField(label=_("Tags"), choices=TAGS)
    baptism_date = forms.DateField(
        input_formats=['%d/%m/%Y'], required=True, label=_('Baptism Date'),
        widget=DatePicker(options={"format": "dd/mm/yyyy"}, format="dd/mm/yyyy", fontawesome=True))

    class Meta:
        model = Publisher
        exclude = ('_id', 'creation_date', 'update_date')
