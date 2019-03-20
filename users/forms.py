from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation
from users.models import UserProfile
from django.contrib.auth.models import User
from congregations.models import Congregation


class FormUser(forms.ModelForm):
    """Form to create/edit user"""

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'is_active', 'is_staff', 'email', 'first_name', 'last_name')


class FormEditUser(forms.ModelForm):
    """Form to create/edit user"""

    class Meta:
        model = User
        fields = ('username', 'is_active', 'is_staff', 'email', 'first_name', 'last_name')


class FormSearchUser(forms.Form):
    def __init__(self, user_profile, *args, **kwargs):
        super(FormSearchUser, self).__init__(*args, **kwargs)
        if user_profile.user.is_staff:
            self.fields['congregation'].queryset = Congregation.objects.all()
        else:
            self.fields['congregation'].queryset = user_profile.congregations.all()
    username = forms.CharField(label=_("Username"), required=False)
    congregation = forms.ModelChoiceField(queryset=Congregation.objects.none(), label=_("Congregation"), required=False)


class FormUserProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('congregation', )
