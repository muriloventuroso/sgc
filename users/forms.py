from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from congregations.models import Congregation, Publisher
from users.models import User


class FormUser(forms.ModelForm):
    """Form to create/edit user"""

    def __init__(self, is_staff, *args, **kwargs):
        super(FormUser, self).__init__(*args, **kwargs)
        if not is_staff:
            del self.fields['is_staff']

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_staff',
                  'first_name', 'last_name', 'congregation', 'publisher')


class FormEditUser(forms.ModelForm):
    """Form to create/edit user"""

    def __init__(self, is_staff, *args, **kwargs):
        super(FormEditUser, self).__init__(*args, **kwargs)
        if not is_staff:
            del self.fields['is_staff']

    class Meta:
        model = User
        fields = ('email', 'is_active', 'is_staff',  'first_name',
                  'last_name', 'congregation', 'publisher')


class FormSearchUser(forms.Form):
    def __init__(self, user_profile, *args, **kwargs):
        super(FormSearchUser, self).__init__(*args, **kwargs)
        if user_profile.is_staff:
            self.fields['congregation'].queryset = Congregation.objects.all()
        else:
            self.fields['congregation'].queryset = Congregation.objects.filter(
                _id=user_profile.congregation_id)
    email = forms.CharField(label=_("Email"), required=False)
    congregation = forms.ModelChoiceField(
        queryset=Congregation.objects.none(), label=_("Congregation"), required=False)
