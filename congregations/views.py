from smtplib import SMTPResponseException
import pymongo
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django_tables2.config import RequestConfig
from congregations.models import Congregation, Group, Publisher, CongregationRole
from congregations.tables import TableCongregations, TableGroups, TablePublishers, TableCongregationRoles
from congregations.forms import (
    FormCongregation, FormGroup, FormPublisher, FormSearchCongregation, FormSearchGroup, FormSearchPublisher,
    FormSearchCongregationRole, FormCongregationRole)
from sgc.helpers import redirect_with_next
from bson.objectid import ObjectId


@login_required
def congregations(request):
    form = FormSearchCongregation(request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'name' in data and data['name']:
            filter_data['name'] = {"$regex": data['name'], '$options': 'i'}
        if 'circuit' in data and data['circuit']:
            filter_data['circuit'] = {
                "$regex": data['circuit'], '$options': 'i'}
        if 'city' in data and data['city']:
            filter_data['city'] = {"$regex": data['city'], '$options': 'i'}
        if 'state' in data and data['state']:
            filter_data['state'] = {"$regex": data['state'], '$options': 'i'}
    if not request.user.is_staff:
        filter_data['_id'] = request.user.congregation_id
    data = Congregation.objects.mongo_find(
        filter_data).sort("name", pymongo.ASCENDING)
    table = TableCongregations(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'congregations/congregations.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'congregations', 'page_title': _("Congregations"),
        'next': request.GET.copy().urlencode()
    })


@login_required
@staff_member_required
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
    congregation = get_object_or_404(
        Congregation, pk=ObjectId(congregation_id))
    if not request.user.is_staff and congregation._id != request.user.congregation_id:
        return SMTPResponseException(status=403)
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
@staff_member_required
def delete_congregation(request, congregation_id):
    congregation = get_object_or_404(
        Congregation, pk=ObjectId(congregation_id))
    congregation.delete()
    messages.success(request, _("Congregation deleted successfully"))
    return redirect_with_next(request, 'congregations')


@login_required
def groups(request):
    form = FormSearchGroup(request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'name' in data and data['name']:
            filter_data['name'] = {"$regex": data['name'], '$options': 'i'}
    filter_data['congregation_id'] = request.user.congregation_id
    data = Group.objects.mongo_find(
        filter_data).sort('name', pymongo.ASCENDING)
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
            item = form.save(commit=False)
            item.congregation_id = request.user.congregation_id
            item.save()
            messages.success(request, _("Group added successfully"))
            return redirect_with_next(request, 'groups')
    else:
        form = FormGroup()
    return render(request, 'groups/add_edit_group.html', {
        'request': request, 'form': form, 'page_group': 'congregations', 'page_title': _("Add Group")
    })


@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, pk=ObjectId(group_id))
    if group.congregation_id != request.user.congregation_id:
        return redirect_with_next(request, 'groups')
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
    group = get_object_or_404(Group, pk=ObjectId(group_id))
    if group.congregation_id != request.user.congregation_id:
        return redirect_with_next(request, 'groups')
    group.delete()
    messages.success(request, _("Group deleted successfully"))
    return redirect_with_next(request, 'groups')


@login_required
def publishers(request):
    form = FormSearchPublisher(request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'name' in data and data['name']:
            filter_data['full_name'] = {
                "$regex": data['name'], '$options': 'i'}
        if 'tags' in data and data['tags']:
            filter_data['tags'] = {"$in": data['tags']}
        if 'group' in data and data['group']:
            filter_data['group_id'] = {"$in": [x["_id"] for x in Group.objects.mongo_find(
                {'name': {"$regex": data['group'], '$options': 'i'}})]}
    filter_data['congregation_id'] = request.user.congregation_id
    data = Publisher.objects.mongo_find(
        filter_data).sort("full_name", pymongo.ASCENDING)
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
        form = FormPublisher(request.user.is_staff,
                             request.user.congregation_id, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            if not request.user.is_staff:
                item.congregation_id = request.user.congregation_id
            item.save()

            messages.success(request, _("Publisher added successfully"))
            return redirect_with_next(request, 'publishers')
    else:
        form = FormPublisher(request.user.is_staff,
                             request.user.congregation_id)
    return render(request, 'publishers/add_edit_publisher.html', {
        'request': request, 'form': form, 'page_group': 'congregations', 'page_title': _("Add Publisher")
    })


@login_required
def edit_publisher(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=ObjectId(publisher_id))
    if publisher.congregation_id != request.user.congregation_id:
        return redirect_with_next(request, 'publishers')
    if request.method == 'POST':
        form = FormPublisher(
            request.user.is_staff, request.user.congregation_id, request.POST, instance=publisher)
        if form.is_valid():
            item = form.save(commit=False)
            if not request.user.is_staff:
                item.congregation_id = request.user.congregation_id
            item.save()
            messages.success(request, _("Publisher edited successfully"))
            return redirect_with_next(request, 'publishers')
    else:
        form = FormPublisher(request.user.is_staff, request.user.congregation_id,
                             instance=publisher, initial={'tags': publisher.tags})
    return render(request, 'publishers/add_edit_publisher.html', {
        'request': request, 'form': form, 'page_group': 'congregations', 'page_title': _("Edit Publisher")
    })


@login_required
def delete_publisher(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=ObjectId(publisher_id))
    if publisher.congregation_id != request.user.congregation_id:
        return redirect_with_next(request, 'publishers')
    publisher.delete()
    messages.success(request, _("Publisher deleted successfully"))
    return redirect_with_next(request, 'publishers')


@login_required
def congregation_roles(request):
    form = FormSearchCongregationRole(request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'role' in data and data['role']:
            filter_data['role'] = data['role']
    filter_data['congregation_id'] = request.user.congregation_id
    data = CongregationRole.objects.filter(**filter_data)
    table = TableCongregationRoles(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'congregations/congregation_roles.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'congregations', 'page_title': _("Congregation Roles"),
        'next': request.GET.copy().urlencode()
    })


@login_required
def add_congregation_role(request):
    if request.method == 'POST':
        form = FormCongregationRole(request.user.congregation_id, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.congregation_id = request.user.congregation_id
            item.save()
            messages.success(request, _(
                "Congregation Role added successfully"))
            return redirect_with_next(request, 'congregation_roles')
    else:
        form = FormCongregationRole()
    return render(request, 'congregations/add_edit_congregation_role.html', {
        'request': request, 'form': form, 'page_group': 'congregations', 'page_title': _("Add Congregation Role")
    })


@login_required
def edit_congregation_role(request, congregation_role_id):
    congregation_role = get_object_or_404(
        CongregationRole, pk=ObjectId(congregation_role_id))
    if congregation_role.congregation_id != request.user.congregation_id:
        return redirect_with_next(request, 'congregation_roles')
    if request.method == 'POST':
        print(request.POST)
        form = FormCongregationRole(
            request.user.congregation_id, request.POST, instance=congregation_role)
        if form.is_valid():
            form.save()
            messages.success(request, _(
                "Congregation Role edited successfully"))
            return redirect_with_next(request, 'congregation_roles')
    else:
        form = FormCongregationRole(
            request.user.congregation_id, instance=congregation_role)
    return render(request, 'congregations/add_edit_congregation_role.html', {
        'request': request, 'form': form, 'page_group': 'congregations', 'page_title': _("Edit Congregation Role")
    })


@login_required
def delete_congregation_role(request, congregation_role_id):
    congregation_role = get_object_or_404(
        CongregationRole, pk=ObjectId(congregation_role_id))
    if congregation_role.congregation_id != request.user.congregation_id:
        return redirect_with_next(request, 'congregation_roles')
    congregation_role.delete()
    messages.success(request, _("Congregation Role deleted successfully"))
    return redirect_with_next(request, 'congregation_roles')
