from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django_tables2.config import RequestConfig
from django.contrib.auth.models import User
from users.models import UserProfile
from users.tables import TableUsers
from users.forms import FormUser, FormSearchUser, FormUserProfile, FormEditUser


@login_required
def users(request):
    profile = UserProfile.objects.get(user=request.user)
    form = FormSearchUser(profile, request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'username' in data and data['username']:
            filter_data['user__username__icontains'] = data['username']
        if 'congregation' in data and data['congregation']:
            filter_data['congregations__in'] = [data['congregation']]
    data = UserProfile.objects.filter(**filter_data)
    table = TableUsers(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'users.html', {
        'request': request, 'table': table, 'app': 'users', 'form': form
    })


@login_required
def add_user(request):
    if request.method == 'POST':
        form = FormUser(request.POST)
        form_profile = FormUserProfile(request.POST)
        if form.is_valid() and form_profile.is_valid():
            user = form.save()
            up = form_profile.save(commit=False)
            up.user = user
            up.save()
            messages.success(request, _("User added successfully"))
            return redirect('users')
    else:
        form = FormUser()
        form_profile = FormUserProfile()
    return render(request, 'add_user.html', {
        'request': request, 'form': form, 'form_profile': form_profile, 'app': 'users'
    })


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    if request.method == 'POST':
        form = FormEditUser(request.POST, instance=user)
        form_profile = FormUserProfile(request.POST, instance=user_profile)
        if form.is_valid() and form_profile.is_valid():
            form.save()
            form_profile.save()
            messages.success(request, _("User edited successfully"))
            return redirect('users')
    else:
        form = FormEditUser(instance=user)
        form_profile = FormUserProfile(instance=user_profile)
    return render(request, 'edit_user.html', {
        'request': request, 'form': form, 'form_profile': form_profile, 'app': 'users'
    })


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, _("User deleted successfully"))
    return redirect('users')
