from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django_tables2.config import RequestConfig
from users.models import User
from users.tables import TableUsers
from users.forms import FormUser, FormSearchUser, FormEditUser
from sgc.helpers import redirect_with_next
from congregations.models import Publisher


@login_required
@staff_member_required
def users(request):
    form = FormSearchUser(request.user, request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if data.get('email'):
            filter_data['_id__in'] = [x["_id"] for x in User.objects.mongo_find({"email": {
                "$regex": data['email'], "$options": "i"}})]
        if data.get('congregation'):
            filter_data['congregation_id'] = data['congregation']
    data = User.objects.select_related("congregation").filter(**filter_data)
    table = TableUsers(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'users.html', {
        'request': request, 'table': table, 'page_group': 'admin', 'page_title': _("Users"), 'form': form,
        'next': request.GET.copy().urlencode()
    })


@login_required
@staff_member_required
def add_user(request):
    if request.method == 'POST':
        form = FormUser(request.user.is_staff, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = form.save()
            user.set_password(data['password'])
            user.save()
            messages.success(request, _("User added successfully"))
            return redirect_with_next(request, 'users')
    else:
        form = FormUser(request.user.is_staff)
    return render(request, 'add_edit_user.html', {
        'request': request, 'form': form,
        'page_group': 'admin', 'page_title': _("Add User")
    })


@login_required
@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = FormEditUser(request.user.is_staff, request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _("User edited successfully"))
            return redirect_with_next(request, 'users')
    else:
        form = FormEditUser(request.user.is_staff, instance=user)

    return render(request, 'add_edit_user.html', {
        'request': request, 'form': form,
        'page_group': 'admin', 'page_title': _("Edit User")
    })


@login_required
@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, _("User deleted successfully"))
    return redirect('users')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _(
                'Your password was successfully updated.'))
            return redirect('users')
        else:
            messages.warning(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form, 'page_group': 'admin', 'page_title': _("Change Password")
    })


@login_required
@staff_member_required
def set_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not request.user.is_staff and user.company != request.user.company:
        return redirect(request, 'users')
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Password was successfully updated.'))
            return redirect_with_next(request, 'users')
        else:
            messages.warning(request, _('Please correct the error below.'))
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'set_password.html', {
        'form': form, 'page_group': 'admin', 'page_title': _("Set Password")
    })


@login_required
def get_resources(request):

    if 'congregation_id' in request.GET and request.GET['congregation_id'] and request.user.is_staff:
        congregation_id = request.GET['congregation_id']
    else:
        congregation_id = request.user.congregation_id

    user_id = None
    if 'user_id' in request.GET and request.GET['user_id']:
        user_id = request.GET['user_id']

    ret = {}
    ret['publishers'] = [
        [x.name, str(x._id), False] for x in Publisher.objects.filter(congregation_id=congregation_id)]

    if user_id:
        user = User.objects.get(_id=user_id)
        for publisher in ret['publishers']:
            if publisher[1] == user.publisher_id:
                publisher[2] = True

    return JsonResponse(ret)
