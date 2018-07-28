from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django_tables2.config import RequestConfig
from congregations.models import Congregation, Group, Publisher
from congregations.tables import TableCongregations, TableGroups, TablePublishers
from congregations.forms import FormCongregation, FormGroup, FormPublisher


@login_required
def congregations(request):
    data = Congregation.objects.all()
    table = TableCongregations(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'congregations/congregations.html', {
        'request': request, 'table': table, 'app': 'congregations'
    })


@login_required
def add_congregation(request):
    if request.method == 'POST':
        form = FormCongregation(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Congregation added successfully"))
            return redirect('congregations')
    else:
        form = FormCongregation()
    return render(request, 'congregations/add_congregation.html', {
        'request': request, 'form': form, 'app': 'congregations'
    })


@login_required
def edit_congregation(request, congregation_id):
    congregation = get_object_or_404(Congregation, pk=congregation_id)
    if request.method == 'POST':
        form = FormCongregation(request.POST, instance=congregation)
        if form.is_valid():
            form.save()
            messages.success(request, _("Congregation edited successfully"))
            return redirect('congregations')
    else:
        form = FormCongregation(instance=congregation)
    return render(request, 'congregations/edit_congregation.html', {
        'request': request, 'form': form, 'app': 'congregations'
    })


@login_required
def delete_congregation(request, congregation_id):
    congregation = get_object_or_404(Congregation, pk=congregation_id)
    congregation.delete()
    messages.success(request, _("Congregation deleted successfully"))
    return redirect('congregations')


@login_required
def groups(request):
    data = Group.objects.all()
    table = TableGroups(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'groups/groups.html', {
        'request': request, 'table': table, 'app': 'congregations'
    })


@login_required
def add_group(request):
    if request.method == 'POST':
        form = FormGroup(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Group added successfully"))
            return redirect('groups')
    else:
        form = FormGroup()
    return render(request, 'groups/add_group.html', {
        'request': request, 'form': form, 'app': 'congregations'
    })


@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        form = FormGroup(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, _("Group edited successfully"))
            return redirect('groups')
    else:
        form = FormGroup(instance=group)
    return render(request, 'groups/edit_group.html', {
        'request': request, 'form': form, 'app': 'congregations'
    })


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group.delete()
    messages.success(request, _("Group deleted successfully"))
    return redirect('groups')


@login_required
def publishers(request):
    data = Publisher.objects.all()
    table = TablePublishers(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'publishers/publishers.html', {
        'request': request, 'table': table, 'app': 'congregations'
    })


@login_required
def add_publisher(request):
    if request.method == 'POST':
        form = FormPublisher(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Publisher added successfully"))
            return redirect('publishers')
    else:
        form = FormPublisher()
    return render(request, 'publishers/add_publisher.html', {
        'request': request, 'form': form, 'app': 'congregations'
    })


@login_required
def edit_publisher(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    if request.method == 'POST':
        form = FormPublisher(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            messages.success(request, _("Publisher edited successfully"))
            return redirect('publishers')
    else:
        form = FormPublisher(instance=publisher, initial={'tags': publisher.tags})
    return render(request, 'publishers/edit_publisher.html', {
        'request': request, 'form': form, 'app': 'congregations'
    })


@login_required
def delete_publisher(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    publisher.delete()
    messages.success(request, _("Publisher deleted successfully"))
    return redirect('publishers')
