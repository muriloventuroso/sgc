from django import forms
from django.utils.translation import gettext_lazy as _
from financial.models import Transaction, TransactionCategory, TRANSACTION_CODE, TRANSACTION_DIRECTION, TRANSACTION_TYPE


class FormTransaction(forms.ModelForm):

    date = forms.DateField(
        label=_("Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))

    class Meta:
        model = Transaction
        exclude = ('_id', 'congregation', 'user',
                   'hide_from_sheet', 'sub_transactions')
        widgets = {'description': forms.TextInput}


class FormSearchTransaction(forms.Form):

    start_date = forms.DateField(
        label=_("Start Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))
    end_date = forms.DateField(
        label=_("End Date"), required=False, input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'date-field'}))
    tc = forms.ChoiceField(label=_("Transaction Code"), choices=[
                           ('', ''), ] + TRANSACTION_CODE, required=False)
    tt = forms.ChoiceField(label=_("Transaction Type"), choices=[
                           ('', ''), ] + TRANSACTION_TYPE, required=False)
    td = forms.ChoiceField(
        label=_("Transaction Direction"), choices=[('', ''), ] + TRANSACTION_DIRECTION, required=False)


class FormGeneratePDF(forms.Form):

    type_pdf = forms.ChoiceField(
        label=_("Type PDF"), choices=[('', ''), ('s26', _("Transaction Sheet")), ('s30', _("Monthly Report"))],
        initial='', required=True)
    month = forms.DateField(
        label=_("Month"), required=True, input_formats=['%Y-%m', '%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'month-field'}))
    balance = forms.DecimalField(label=_("Balance"), required=False)


class FormOffTransaction(forms.Form):
    deposits = forms.DecimalField(
        label=_("Off Deposits"), required=False,
        help_text=_("Deposits recorded in the Transaction Sheet but not appearing on the statement"))
    bank_fees = forms.DecimalField(
        label=_("Bank Fees"), required=False,
        help_text=_("Bank Fees Not Recorded on Transaction Sheet"))
    bank_interest = forms.DecimalField(
        label=_("Bank Interest"), required=False,
        help_text=_("Bank Interest Not Recorded on Transaction Sheet"))
    eletronic = forms.DecimalField(
        label=_("Eletronic Donates"), required=False,
        help_text=_("Donations made electronically unregistered in the Transaction Sheet"))


class FormUnverifiedChecks(forms.Form):
    n_confirmation = forms.CharField(
        label=_("Número de Confirmação"), required=False)
    value = forms.DecimalField(label=_("Value"), required=False)


class FormTransactionCategory(forms.ModelForm):

    class Meta:
        model = TransactionCategory
        exclude = ('_id', 'congregation', 'user')


class FormSearchTransactionCategory(forms.Form):
    name = forms.CharField(label=_("Name"), required=False)


class FormMonthlySummary(forms.Form):

    month = forms.DateField(
        label=_("Month"), required=False, input_formats=['%Y-%m', '%m/%Y'],
        widget=forms.widgets.DateInput(attrs={'class': 'month-field'}))
