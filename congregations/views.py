from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django_tables2.config import RequestConfig
from congregations.models import Congregation, Group, Publisher
from congregations.tables import TableCongregations, TableGroups, TablePublishers
from congregations.forms import (
    FormCongregation, FormGroup, FormPublisher, FormSearchCongregation, FormSearchGroup, FormSearchPublisher)
from users.models import UserProfile
from sgc.helpers import redirect_with_next


@login_required
def congregations(request):
    profile = UserProfile.objects.get(user=request.user)
    form = FormSearchCongregation(request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'name' in data and data['name']:
            filter_data['name__icontains'] = data['name']
        if 'circuit' in data and data['circuit']:
            filter_data['circuit__icontains'] = data['circuit']
        if 'city' in data and data['city']:
            filter_data['city__icontains'] = data['city']
        if 'state' in data and data['state']:
            filter_data['state__icontains'] = data['state']
    if not request.user.is_staff:
        filter_data['congregation_id'] = profile.congregation_id
    data = Congregation.objects.filter(**filter_data)
    table = TableCongregations(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'congregations/congregations.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'congregations', 'page_title': _("Congregations"),
        'next': request.GET.copy().urlencode()
    })


@login_required
def add_congregation(request):
    if request.method == 'POST':
        form = FormCongregation(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Congregation added successfully"))
            return redirect_with_next(request, 'congregations')
    else:
        form = FormCongregation()
    return render(request, 'congregations/add_edit_congregation.html', {
        'request': request, 'form': form, 'page_group': 'congregations', 'page_title': _("Add Congregation")
    })


@login_required
def edit_congregation(request, congregation_id):
    congregation = get_object_or_404(Congregation, pk=congregation_id)
    if request.method == 'POST':
        form = FormCongregation(request.POST, instance=congregation)
        if form.is_valid():
            form.save()
            messages.success(request, _("Congregation edited successfully"))
            return redirect_with_next(request, 'congregations')
    else:
        form = FormCongregation(instance=congregation)
    return render(request, 'congregations/add_edit_congregation.html', {
        'request': request, 'form': form, 'page_group': 'congregations', 'page_title': _("Edit Congregation")
    })


@login_required
def delete_congregation(request, congregation_id):
    congregation = get_object_or_404(Congregation, pk=congregation_id)
    congregation.delete()
    messages.success(request, _("Congregation deleted successfully"))
    return redirect_with_next(request, 'congregations')


@login_required
def groups(request):
    profile = UserProfile.objects.get(user=request.user)
    form = FormSearchGroup(request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'name' in data and data['name']:
            filter_data['name__icontains'] = data['name']
    if not request.user.is_staff:
        filter_data['congregation_id'] = profile.congregation_id
    data = Group.objects.filter(**filter_data)
    table = TableGroups(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'groups/groups.html', {
        'request': request, 'table': table, 'page_group': 'congregations', 'page_title': _("Groups"),
        'form': form, 'next': request.GET.copy().urlencode()
    })


@login_required
def add_group(request):
    if request.method == 'POST':
        form = FormGroup(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Group added successfully"))
            return redirect_with_next(request, 'groups')
    else:
        form = FormGroup()
    return render(request, 'groups/add_edit_group.html', {
        'request': request, 'form': form, 'page_group': 'congregations', 'page_title': _("Add Group")
    })


@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        form = FormGroup(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, _("Group edited successfully"))
            return redirect_with_next(request, 'groups')
    else:
        form = FormGroup(instance=group)
    return render(request, 'groups/add_edit_group.html', {
        'request': request, 'form': form, 'page_group': 'congregations', 'page_title': _("Edit Group")
    })


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group.delete()
    messages.success(request, _("Group deleted successfully"))
    return redirect_with_next(request, 'groups')


@login_required
def publishers(request):
    profile = UserProfile.objects.get(user=request.user)
    form = FormSearchPublisher(profile, request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'name' in data and data['name']:
            filter_data['full_name__icontains'] = data['name']
        if 'tags' in data and data['tags']:
            filter_data['tags__in'] = data['tags']
        if 'group' in data and data['group']:
            filter_data['group__name__icontains'] = data['group']
    if not request.user.is_staff:
        filter_data['congregation_id'] = profile.congregation_id
    data = Publisher.objects.filter(**filter_data)
    table = TablePublishers(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'publishers/publishers.html', {
        'request': request, 'table': table, 'page_group': 'congregations', 'page_title': _("Publishers"), 'form': form,
        'next': request.GET.copy().urlencode()
    })


@login_required
def add_publisher(request):
    if request.method == 'POST':
        form = FormPublisher(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Publisher added successfully"))
            return redirect_with_next(request, 'publishers')
    else:
        form = FormPublisher()
    return render(request, 'publishers/add_edit_publisher.html', {
        'request': request, 'form': form, 'page_group': 'congregations', 'page_title': _("Add Publisher")
    })


@login_required
def edit_publisher(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    if request.method == 'POST':
        form = FormPublisher(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            messages.success(request, _("Publisher edited successfully"))
            return redirect_with_next(request, 'publishers')
    else:
        form = FormPublisher(instance=publisher, initial={'tags': publisher.tags})
    return render(request, 'publishers/add_edit_publisher.html', {
        'request': request, 'form': form, 'page_group': 'congregations', 'page_title': _("Edit Publisher")
    })


@login_required
def delete_publisher(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    publisher.delete()
    messages.success(request, _("Publisher deleted successfully"))
    return redirect_with_next(request, 'publishers')
