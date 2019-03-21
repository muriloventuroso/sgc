import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django_tables2.config import RequestConfig
from preaching.models import Pioneer
from preaching.tables import TablePioneers
from preaching.forms import FormPioneer, FormSearchPioneer
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
        form = FormPioneer(request.LANGUAGE_CODE, request.POST)
        if form.is_valid():
            pioneer = form.save(commit=False)
            pioneer.congregation_id = profile.congregation_id
            pioneer.save()
            messages.success(request, _("Pioneer added successfully"))
            return redirect_with_next(request, 'pioneers')
    else:
        form = FormPioneer(request.LANGUAGE_CODE)
    return render(request, 'add_edit_pioneer.html', {
        'request': request, 'form': form, 'page_group': 'preaching', 'page_title': _("Add Pioneer")
    })


@login_required
def edit_pioneer(request, pioneer_id):
    pioneer = get_object_or_404(Pioneer, pk=pioneer_id)
    if request.method == 'POST':
        form = FormPioneer(request.LANGUAGE_CODE, request.POST, instance=pioneer)
        if form.is_valid():
            form.save()
            messages.success(request, _("Pioneer edited successfully"))
            return redirect_with_next(request, 'pioneers')
    else:
        form = FormPioneer(instance=pioneer)
    return render(request, 'add_edit_pioneer.html', {
        'request': request, 'form': form, 'page_group': 'preaching', 'page_title': _("Edit Pioneer")
    })


@login_required
def delete_pioneer(request, pioneer_id):
    pioneer = get_object_or_404(Pioneer, pk=pioneer_id)
    pioneer.delete()
    messages.success(request, _("Pioneer deleted successfully"))
    return redirect_with_next(request, 'pioneers')
