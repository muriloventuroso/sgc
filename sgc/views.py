from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import HttpResponseRedirect


@login_required
def home(request):

    return render(request, 'home.html', {
        'request': request
    })


def login(request):
    """Make login."""

    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_page = request.GET.get('next', '/')
            split_next = [i for i in next_page.split('/') if i != '']
            if split_next:
                next_page = '/'.join(split_next[1:])
            else:
                next_page = ''
            return HttpResponseRedirect('/' + next_page)

    return render(request, 'login.html', {
        'request': request,
        'form': form,
        'next': request.GET.get('next', '/')
    })
