import datetime
import calendar
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django_tables2.config import RequestConfig
from django_tables2 import Column
from financial.models import Transaction, TransactionCategory, MonthlySummary
from financial.tables import TableTransactions, TableTransactionCategories, TableMonthlySummary
from financial.forms import (
    FormTransaction, FormSearchTransaction, FormGeneratePDF, FormSearchTransactionCategory, FormTransactionCategory,
    FormMonthlySummary)
from financial.helpers import TransactionSheetPdf, MonthlyReportPdf
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
            filter_data['date__gte'] = datetime.datetime.now().replace(day=1)
        if 'end_date' in data and data['end_date']:
            filter_data['date__lte'] = data['end_date']
        if 'description' in data and data['description']:
            filter_data['description__icontains'] = data['descriptions']
        if 'tc' in data and data['tc']:
            filter_data['tc'] = data['tc']
        if 'tt' in data and data['tt']:
            filter_data['tt'] = data['tt']
        if 'td' in data and data['td']:
            filter_data['td'] = data['td']
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
            transaction.date = transaction.date + datetime.timedelta(hours=6)
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


@login_required
def generate_pdf(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FormGeneratePDF(request.LANGUAGE_CODE, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['type_pdf'] == 's26':
                s26 = TransactionSheetPdf(data['month'], data['balance'], profile.congregation_id)
                s26.generate()
                pdf_file = s26.save()

                response = HttpResponse(pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="' + str(_("Transaction Sheet")) + '.pdf"'
                return response
            elif data['type_pdf'] == 's30':
                s30 = MonthlyReportPdf(data['month'], data['balance'], profile.congregation_id)
                s30.generate()
                pdf_file = s30.save()

                response = HttpResponse(pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="' + str(_("Monthly Report")) + '.pdf"'
                return response
        else:
            print(form.errors)

    else:
        form = FormGeneratePDF(request.LANGUAGE_CODE)
    return render(request, 'generate_pdf.html', {
        'request': request, 'form': form, 'page_group': 'financial', 'page_title': _("Generate PDF"),
    })


@login_required
def transactioncategories(request):
    profile = UserProfile.objects.get(user=request.user)
    form = FormSearchTransactionCategory(request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'name' in data and data['name']:
            filter_data['name__icontains'] = data['name']
    if not request.user.is_staff:
        filter_data['congregation_id'] = profile.congregation_id
    data = TransactionCategory.objects.filter(**filter_data)
    table = TableTransactionCategories(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'transactioncategories.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'financial', 'page_title': _("Transaction Categories"),
        'next': request.GET.copy().urlencode()
    })


@login_required
def add_transactioncategory(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FormTransactionCategory(request.POST)
        if form.is_valid():
            transactioncategory = form.save(commit=False)
            transactioncategory.congregation_id = profile.congregation_id
            transactioncategory.user = request.user
            transactioncategory.save()
            messages.success(request, _("Transaction Category added successfully"))
            return redirect_with_next(request, 'transactioncategories')
    else:
        form = FormTransactionCategory()
    return render(request, 'add_edit_transactioncategory.html', {
        'request': request, 'form': form, 'page_group': 'financial', 'page_title': _("Add Transaction Category")
    })


@login_required
def edit_transactioncategory(request, category_id):
    transactioncategory = get_object_or_404(TransactionCategory, pk=category_id)
    if request.method == 'POST':
        form = FormTransactionCategory(request.POST, instance=transactioncategory)
        if form.is_valid():
            form.save()
            messages.success(request, _("Transaction Category edited successfully"))
            return redirect_with_next(request, 'transactioncategories')
    else:
        form = FormTransactionCategory(instance=transactioncategory)
    return render(request, 'add_edit_transactioncategory.html', {
        'request': request, 'form': form, 'page_group': 'financial', 'page_title': _("Edit Transaction Category")
    })


@login_required
def delete_transactioncategory(request, category_id):
    transactioncategory = get_object_or_404(TransactionCategory, pk=category_id)
    transactioncategory.delete()
    messages.success(request, _("Transaction Category deleted successfully"))
    return redirect_with_next(request, 'transactioncategories')


@login_required
def monthly_summary(request):
    profile = UserProfile.objects.get(user=request.user)
    form = FormMonthlySummary(request.LANGUAGE_CODE, request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'month' in data and data['month']:
            start_date = datetime.datetime.combine(data['month'], datetime.time.min)
            last_day = calendar.monthrange(start_date.year, start_date.month)[1]
            end_date = datetime.datetime.combine(start_date.replace(day=last_day), datetime.time.max)
            filter_data["date__range"] = [start_date, end_date]

    if not request.user.is_staff:
        filter_data['congregation_id'] = profile.congregation_id
    data_db = MonthlySummary.objects.filter(**filter_data)
    data = []
    extra_columns = []
    tcs = {}
    for d in data_db:
        item = {
            'date': d.date.strftime("%m/%Y"),
            'carried_balance': d.carried_balance,
            'final_balance': d.final_balance
        }
        for t in d.transactions:
            if t.tc not in tcs:
                tcs[t.tc] = {'name': t.get_tc_display()}
            item[t.tc] = t.value
        data.append(item)

    for key, value in tcs.items():
        extra_columns.append((key, Column(verbose_name=value['name'])))
    table = TableMonthlySummary(data, extra_columns=extra_columns)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'monthly_summary.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'financial', 'page_title': _("Monthly Summary"),
        'next': request.GET.copy().urlencode()
    })
