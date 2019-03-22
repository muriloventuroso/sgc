import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django_tables2.config import RequestConfig
from preaching.models import Pioneer, FieldServiceReport
from preaching.tables import TablePioneers, TableFieldServiceReports
from preaching.forms import FormPioneer, FormSearchPioneer, FormSearchFieldServiceReport, FormFieldServiceReport
from sgc.helpers import redirect_with_next
from users.models import UserProfile


@login_required
def pioneers(request):
    profile = UserProfile.objects.get(user=request.user)
    form = FormSearchPioneer(request.LANGUAGE_CODE, request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'start_date' in data and data['start_date']:
            filter_data['start_date__gte'] = data['start_date']
        else:
            filter_data['start_date__gte'] = datetime.datetime.now()
        if 'end_date' in data and data['end_date']:
            filter_data['start_date__lte'] = data['end_date']
    if not request.user.is_staff:
        filter_data['congregation_id'] = profile.congregation_id
    data = Pioneer.objects.filter(**filter_data)
    table = TablePioneers(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'pioneers.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'preaching', 'page_title': _("Pioneers"),
        'next': request.GET.copy().urlencode()
    })


@login_required
def add_pioneer(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FormPioneer(profile.congregation_id, request.LANGUAGE_CODE, request.POST)
        if form.is_valid():
            pioneer = form.save(commit=False)
            pioneer.congregation_id = profile.congregation_id
            pioneer.save()
            messages.success(request, _("Pioneer added successfully"))
            return redirect_with_next(request, 'pioneers')
    else:
        form = FormPioneer(profile.congregation_id, request.LANGUAGE_CODE)
    return render(request, 'add_edit_pioneer.html', {
        'request': request, 'form': form, 'page_group': 'preaching', 'page_title': _("Add Pioneer")
    })


@login_required
def edit_pioneer(request, pioneer_id):
    pioneer = get_object_or_404(Pioneer, pk=pioneer_id)
    if request.method == 'POST':
        form = FormPioneer(pioneer.congregation_id, request.LANGUAGE_CODE, request.POST, instance=pioneer)
        if form.is_valid():
            form.save()
            messages.success(request, _("Pioneer edited successfully"))
            return redirect_with_next(request, 'pioneers')
    else:
        form = FormPioneer(pioneer.congregation_id, request.LANGUAGE_CODE, instance=pioneer)
    return render(request, 'add_edit_pioneer.html', {
        'request': request, 'form': form, 'page_group': 'preaching', 'page_title': _("Edit Pioneer")
    })


@login_required
def delete_pioneer(request, pioneer_id):
    pioneer = get_object_or_404(Pioneer, pk=pioneer_id)
    pioneer.delete()
    messages.success(request, _("Pioneer deleted successfully"))
    return redirect_with_next(request, 'pioneers')


@login_required
def field_service_reports(request):
    profile = UserProfile.objects.get(user=request.user)
    form = FormSearchFieldServiceReport(profile.congregation_id, request.LANGUAGE_CODE, request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'start_date' in data and data['start_date']:
            filter_data['date__gte'] = data['start_date']
        if 'end_date' in data and data['end_date']:
            filter_data['date__lte'] = data['end_date']
        if 'publisher' in data and data['publisher']:
            filter_data['publisher'] = data['publisher']
    if not request.user.is_staff:
        filter_data['congregation_id'] = profile.congregation_id
    data = FieldServiceReport.objects.filter(**filter_data)
    table = TableFieldServiceReports(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'field_service_reports.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'preaching', 'page_title': _("Field Service Reports"),
        'next': request.GET.copy().urlencode()
    })


@login_required
def add_field_service_report(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FormFieldServiceReport(profile.congregation_id, request.LANGUAGE_CODE, request.POST)
        if form.is_valid():
            field_service_report = form.save(commit=False)
            field_service_report.congregation_id = profile.congregation_id
            field_service_report.save()
            messages.success(request, _("Field Service Report added successfully"))
            return redirect_with_next(request, 'field_service_reports')
    else:
        form = FormFieldServiceReport(profile.congregation_id, request.LANGUAGE_CODE)
    return render(request, 'add_edit_field_service_report.html', {
        'request': request, 'form': form, 'page_group': 'preaching', 'page_title': _("Add Field Service Report")
    })


@login_required
def edit_field_service_report(request, field_service_report_id):
    field_service_report = get_object_or_404(FieldServiceReport, pk=field_service_report_id)
    if request.method == 'POST':
        form = FormFieldServiceReport(
            field_service_report.congregation_id, request.LANGUAGE_CODE, request.POST, instance=field_service_report)
        if form.is_valid():
            form.save()
            messages.success(request, _("Field Service Report edited successfully"))
            return redirect_with_next(request, 'field_service_reports')
    else:
        form = FormFieldServiceReport(
            field_service_report.congregation_id, request.LANGUAGE_CODE, instance=field_service_report)
    return render(request, 'add_edit_field_service_report.html', {
        'request': request, 'form': form, 'page_group': 'preaching', 'page_title': _("Edit Field Service Report")
    })


@login_required
def delete_field_service_report(request, field_service_report_id):
    field_service_report = get_object_or_404(FieldServiceReport, pk=field_service_report_id)
    field_service_report.delete()
    messages.success(request, _("FieldServiceReport deleted successfully"))
    return redirect_with_next(request, 'field_service_reports')
