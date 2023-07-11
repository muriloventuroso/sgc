import datetime
import calendar
from collections import Counter
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django_tables2.config import RequestConfig
from django_tables2 import Column
from financial.models import Transaction, TransactionCategory, MonthlySummary, SubTransaction
from financial.tables import TableTransactions, TableTransactionCategories, TableMonthlySummary, TableConfrontation
from financial.forms import (
    FormTransaction, FormSearchTransaction, FormGeneratePDF, FormSearchTransactionCategory, FormTransactionCategory,
    FormMonthlySummary, FormUnverifiedChecks, FormOffTransaction)
from financial.helpers import TransactionSheetPdf, MonthlyReportPdf
from sgc.helpers import redirect_with_next
from bson.objectid import ObjectId


@login_required
def transactions(request):
    form = FormSearchTransaction(request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'start_date' in data and data['start_date']:
            filter_data['date__gte'] = data['start_date']
        else:
            filter_data['date__gte'] = datetime.datetime.now().replace(day=1)
        if 'end_date' in data and data['end_date']:
            filter_data['date__lte'] = data['end_date']
        if 'tc' in data and data['tc']:
            filter_data['tc'] = data['tc']
        if 'tt' in data and data['tt']:
            filter_data['tt'] = data['tt']
        if 'td' in data and data['td']:
            filter_data['td'] = data['td']
    filter_data['congregation_id'] = request.user.congregation_id
    summary = {}
    data = Transaction.objects.filter(**filter_data).select_related('category')
    new_data = []
    for t in data:
        new_data.append({
            'pk': t.pk,
            'date': t.date,
            'description': t.description,
            'tc': t.get_tc_display(),
            'td': t.get_td_display(),
            'tt': t.get_tt_display(),
            'category': str(t.category) if t.category else "",
            'value': t.value
        })
        if t.tc:
            if t.tc not in summary:
                summary[t.tc] = {'name': t.get_tc_display(), 'value': 0}
            summary[t.tc]['value'] += t.value
        if t.sub_transactions:
            for s in t.sub_transactions:
                new_data.append({
                    'date': s.date,
                    'description': s.description,
                    'tc': s.get_tc_display(),
                    'td': s.get_td_display(),
                    'tt': s.get_tt_display(),
                    'category': str(s.category) if s.category else "",
                    'value': s.value
                })
                if s.tc:
                    if s.tc not in summary:
                        summary[s.tc] = {
                            'name': s.get_tc_display(), 'value': 0}
                    summary[s.tc]['value'] += s.value
    table = TableTransactions(new_data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'transactions.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'financial', 'page_title': _("Transactions"),
        'next': request.GET.copy().urlencode(),
        'summary': summary
    })


@login_required
def add_transaction(request):
    if request.method == 'POST':
        transactions = []
        tops = {}
        last_date = None
        for i, date in enumerate(request.POST.getlist('date')):
            category = request.POST.getlist('category')[i]
            top_id = request.POST.getlist('top_id')[i]
            if not date and top_id and last_date:
                date = last_date
            last_date = date
            if request.LANGUAGE_CODE == 'en':
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
            else:
                date = datetime.datetime.strptime(date, '%d/%m/%Y')
            transactions.append({
                'date': date,
                'description': request.POST.getlist('description')[i],
                'tc': request.POST.getlist('tc')[i],
                'td': request.POST.getlist('td')[i],
                'tt': request.POST.getlist('tt')[i],
                'value': float(request.POST.getlist('value')[i]),
                'category_id': category if category else None,
                'id': request.POST.getlist('id')[i],
                'top_id': request.POST.getlist('top_id')[i]
            })
        for transaction in [x for x in transactions if x['top_id']]:
            if transaction['top_id'] not in tops:
                tops[transaction['top_id']] = []
            tops[transaction['top_id']].append(SubTransaction(
                date=transaction['date'],
                description=transaction['description'],
                tc=transaction['tc'],
                td=transaction['td'],
                tt=transaction['tt'],
                value=float(transaction['value']),
                category_id=transaction['category_id']
            ))
        for transaction in [x for x in transactions if not x['top_id']]:
            if transaction['id'] in tops:
                subs = tops[transaction['id']]
                value = sum([float(x.value) for x in subs])
            else:
                subs = []
                value = transaction['value']
            Transaction(
                date=transaction['date'],
                description=transaction['description'],
                tc=transaction['tc'],
                td=transaction['td'],
                tt=transaction['tt'],
                value=float(value),
                category_id=transaction['category_id'],
                sub_transactions=subs,
                congregation_id=request.user.congregation_id,
                user=request.user
            ).save()

        messages.success(request, _("Transaction added successfully"))
        return redirect_with_next(request, 'transactions')
    else:
        form = FormTransaction()
    return render(request, 'add_transactions.html', {
        'request': request, 'form': form, 'page_group': 'financial', 'page_title': _("Add Transactions")
    })


@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=ObjectId(transaction_id))
    if request.method == 'POST':

        transaction.sub_transactions = []
        last_date = None
        print(request.POST)
        for i, date in enumerate(request.POST.getlist('date')):
            category = request.POST.getlist('category')[i]
            if not date and last_date:
                date = last_date
            last_date = date
            if request.LANGUAGE_CODE == 'en':
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
            else:
                date = datetime.datetime.strptime(date, '%d/%m/%Y')
            item = {
                'date': date,
                'description': request.POST.getlist('description')[i],
                'tc': request.POST.getlist('tc')[i],
                'td': request.POST.getlist('td')[i],
                'tt': request.POST.getlist('tt')[i],
                'value': float(request.POST.getlist('value')[i]),
                'category_id': category if category else None
            }
            if i == 0:
                transaction.date = item['date']
                transaction.description = item['description']
                transaction.tc = item['tc']
                transaction.td = item['td']
                transaction.tt = item['tt']
                transaction.value = float(item['value'])
                transaction.category_id = item['category_id']
            else:
                transaction.sub_transactions.append(SubTransaction(**item))
        if transaction.sub_transactions:
            transaction.value = sum([float(x.value)
                                    for x in transaction.sub_transactions])
        transaction.save()
        messages.success(request, _("Transaction edited successfully"))
        return redirect_with_next(request, 'transactions')

    form = FormTransaction(instance=transaction)
    new_form = FormTransaction()
    sub_transactions = []
    for s in transaction.sub_transactions:
        sub_transactions.append(FormTransaction(
            instance=s))
    return render(request, 'edit_transaction.html', {
        'request': request, 'form': form, 'page_group': 'financial', 'page_title': _("Edit Transaction"),
        'transaction': transaction, 'new_form': new_form, 'sub_transactions': sub_transactions
    })


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=ObjectId(transaction_id))
    transaction.delete()
    messages.success(request, _("Transaction deleted successfully"))
    return redirect_with_next(request, 'transactions')


@login_required
def generate_pdf(request):
    if request.method == 'POST':
        form = FormGeneratePDF(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['type_pdf'] == 's26':
                checks = []
                for i, n_confirmaation in enumerate(request.POST.getlist('n_confirmation')):
                    checks.append({
                        'n_confirmation': n_confirmaation,
                        'value': request.POST.getlist('value')[i]
                    })
                data_off = {}
                formOffTransaction = FormOffTransaction(request.POST)
                if formOffTransaction.is_valid():
                    data_off = formOffTransaction.cleaned_data
                s26 = TransactionSheetPdf(
                    data['month'], data['balance'], request.user.congregation_id, checks, data_off)
                s26.generate()
                pdf_file = s26.save()

                response = HttpResponse(
                    pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="' + \
                    's26.pdf"'
                return response
            elif data['type_pdf'] == 's30':
                s30 = MonthlyReportPdf(
                    data['month'], data['balance'], request.user.congregation_id)
                s30.generate()
                pdf_file = s30.save()

                response = HttpResponse(
                    pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="' + \
                    's30.pdf"'
                return response
        else:
            print(form.errors)

    else:
        form = FormGeneratePDF()
    formChecks = FormUnverifiedChecks()
    formOffTransaction = FormOffTransaction()
    return render(request, 'pdf_financial.html', {
        'request': request, 'form': form, 'page_group': 'financial', 'page_title': _("Generate PDF"),
        'formChecks': formChecks, 'formOffTransaction': formOffTransaction
    })


@login_required
def transactioncategories(request):
    form = FormSearchTransactionCategory(request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'name' in data and data['name']:
            filter_data['name__icontains'] = data['name']
    if not request.user.is_staff:
        filter_data['congregation_id'] = request.user.congregation_id
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
    if request.method == 'POST':
        form = FormTransactionCategory(request.POST)
        if form.is_valid():
            transactioncategory = form.save(commit=False)
            transactioncategory.congregation_id = request.user.congregation_id
            transactioncategory.user = request.user
            transactioncategory.save()
            messages.success(request, _(
                "Transaction Category added successfully"))
            return redirect_with_next(request, 'transactioncategories')
    else:
        form = FormTransactionCategory()
    return render(request, 'add_edit_transactioncategory.html', {
        'request': request, 'form': form, 'page_group': 'financial', 'page_title': _("Add Transaction Category")
    })


@login_required
def edit_transactioncategory(request, category_id):
    transactioncategory = get_object_or_404(
        TransactionCategory, pk=ObjectId(category_id))
    if request.method == 'POST':
        form = FormTransactionCategory(
            request.POST, instance=transactioncategory)
        if form.is_valid():
            form.save()
            messages.success(request, _(
                "Transaction Category edited successfully"))
            return redirect_with_next(request, 'transactioncategories')
    else:
        form = FormTransactionCategory(instance=transactioncategory)
    return render(request, 'add_edit_transactioncategory.html', {
        'request': request, 'form': form, 'page_group': 'financial', 'page_title': _("Edit Transaction Category")
    })


@login_required
def delete_transactioncategory(request, category_id):
    transactioncategory = get_object_or_404(
        TransactionCategory, pk=ObjectId(category_id))
    transactioncategory.delete()
    messages.success(request, _("Transaction Category deleted successfully"))
    return redirect_with_next(request, 'transactioncategories')


@login_required
def monthly_summary(request):
    form = FormMonthlySummary(request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'month' in data and data['month']:
            start_date = datetime.datetime.combine(
                data['month'], datetime.time.min)
            last_day = calendar.monthrange(
                start_date.year, start_date.month)[1]
            end_date = datetime.datetime.combine(
                start_date.replace(day=last_day), datetime.time.max)
            filter_data["date__range"] = [start_date, end_date]

    if not request.user.is_staff:
        filter_data['congregation_id'] = request.user.congregation_id
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


@login_required
def confrontation(request):
    form = FormMonthlySummary(request.GET)
    count = None
    if request.GET:
        if form.is_valid():
            data = form.cleaned_data
            if 'month' in data and data['month']:
                start_date = datetime.datetime.combine(
                    data['month'], datetime.time.min)
                last_day = calendar.monthrange(
                    start_date.year, start_date.month)[1]
                end_date = datetime.datetime.combine(
                    start_date.replace(day=last_day), datetime.time.max)
                data_db = list(Transaction.objects.mongo_aggregate([

                    {"$match": {
                        "date": {"$gte": start_date, '$lte': end_date},
                        "congregation_id": request.user.congregation_id,
                        "hide_from_sheet": False}},
                    {
                        "$group": {
                            "_id": None,
                            "sum_receipts_in": {
                                "$sum": {
                                    "$cond": [{"$and": [{"$eq": ["$td", "I"]}, {"$eq": ["$tt", "R"]}]}, "$value", 0]
                                }
                            },
                            "sum_receipts_out": {
                                "$sum": {
                                    "$cond": [{"$and": [{"$eq": ["$td", "O"]}, {"$eq": ["$tt", "R"]}]}, "$value", 0]
                                }
                            },
                            "sum_account_in": {
                                "$sum": {
                                    "$cond": [{"$and": [{"$eq": ["$td", "I"]}, {"$eq": ["$tt", "C"]}]}, "$value", 0]
                                }
                            },
                            "sum_account_out": {
                                "$sum": {
                                    "$cond": [{"$and": [{"$eq": ["$td", "O"]}, {"$eq": ["$tt", "C"]}]}, "$value", 0]
                                }
                            },
                        }
                    }
                ]))
                data_db2 = list(Transaction.objects.mongo_aggregate([
                    {"$unwind": "$sub_transactions"},
                    {"$match": {
                        "sub_transactions.description": "",
                        "date": {"$gte": start_date, '$lte': end_date},
                        "congregation_id": request.user.congregation_id,
                        "hide_from_sheet": False}},
                    {
                        "$group": {
                            "_id": None,
                            "sum_receipts_in": {
                                "$sum": {
                                    "$cond": [
                                        {"$and": [
                                            {"$eq": [
                                                "$sub_transactions.td", "I"]},
                                            {"$eq": [
                                                "$sub_transactions.tt", "R"]}
                                        ]}, "$sub_transactions.value", 0]
                                }
                            },
                            "sum_receipts_out": {
                                "$sum": {
                                    "$cond": [
                                        {"$and": [
                                            {"$eq": [
                                                "$sub_transactions.td", "O"]},
                                            {"$eq": [
                                                "$sub_transactions.tt", "R"]}
                                        ]}, "$sub_transactions.value", 0]
                                }
                            },
                            "sum_account_in": {
                                "$sum": {
                                    "$cond": [
                                        {"$and": [
                                            {"$eq": [
                                                "$sub_transactions.td", "I"]},
                                            {"$eq": [
                                                "$sub_transactions.tt", "C"]}
                                        ]}, "$sub_transactions.value", 0]
                                }
                            },
                            "sum_account_out": {
                                "$sum": {
                                    "$cond": [
                                        {"$and": [
                                            {"$eq": [
                                                "$sub_transactions.td", "O"]},
                                            {"$eq": [
                                                "$sub_transactions.tt", "C"]}
                                        ]}, "$sub_transactions.value", 0]
                                }
                            },
                        }
                    }
                ]))
                datas_db = []
                if data_db:
                    data_db = dict(data_db[0])
                    del data_db['_id']
                    datas_db.append(data_db)
                if data_db2:
                    data_db2 = dict(data_db2[0])
                    del data_db2['_id']
                    datas_db.append(data_db2)
                count = Counter()
                for d in datas_db:
                    count.update(d)
                count = dict(count)
                if count:
                    count['month'] = data['month'].strftime("%m/%Y")
                    count['receipts_final_balance'] = (
                        count['sum_receipts_in'] - count['sum_receipts_out'])
                    summary = MonthlySummary.objects.filter(
                        congregation_id=request.user.congregation_id,
                        date__range=[
                            start_date - relativedelta(months=1),
                            end_date - relativedelta(months=1)]).first()
                    if summary:
                        balance = float(summary.final_balance)
                        count['account_carried_balance'] = balance
                        count['account_final_balance'] = (
                            balance + count['sum_account_in'] - count['sum_account_out'])
    if count:
        data_table = [count]
    else:
        data_table = []
    table = TableConfrontation(data_table)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'confrontation.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'financial', 'page_title': _("Confrontation"),
        'next': request.GET.copy().urlencode()
    })
