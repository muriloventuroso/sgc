import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django_tables2.config import RequestConfig
from financial.models import Transaction
from financial.tables import TableTransactions
from financial.forms import FormTransaction, FormSearchTransaction
from sgc.helpers import redirect_with_next
from users.models import UserProfile


@login_required
def transactions(request):
    profile = UserProfile.objects.get(user=request.user)
    form = FormSearchTransaction(request.LANGUAGE_CODE, request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'start_date' in data and data['start_date']:
            filter_data['date__gte'] = data['start_date']
        else:
            filter_data['date__gte'] = datetime.datetime.now()
        if 'end_date' in data and data['end_date']:
            filter_data['date__lte'] = data['end_date']
    if not request.user.is_staff:
        filter_data['congregation_id'] = profile.congregation_id
    data = Transaction.objects.filter(**filter_data)
    table = TableTransactions(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'transactions.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'financial', 'page_title': _("Transactions"),
        'next': request.GET.copy().urlencode()
    })


@login_required
def add_transaction(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FormTransaction(request.LANGUAGE_CODE, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.congregation_id = profile.congregation_id
            transaction.user = request.user
            transaction.save()
            messages.success(request, _("Transaction added successfully"))
            return redirect_with_next(request, 'transactions')
    else:
        form = FormTransaction(request.LANGUAGE_CODE)
    return render(request, 'add_edit_transaction.html', {
        'request': request, 'form': form, 'page_group': 'financial', 'page_title': _("Add Transaction")
    })


@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if request.method == 'POST':
        form = FormTransaction(request.LANGUAGE_CODE, request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, _("Transaction edited successfully"))
            return redirect_with_next(request, 'transactions')
    else:
        form = FormTransaction(request.LANGUAGE_CODE, instance=transaction)
    return render(request, 'add_edit_transaction.html', {
        'request': request, 'form': form, 'page_group': 'financial', 'page_title': _("Edit Transaction")
    })


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    transaction.delete()
    messages.success(request, _("Transaction deleted successfully"))
    return redirect_with_next(request, 'transactions')
