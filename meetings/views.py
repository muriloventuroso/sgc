from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django_tables2.config import RequestConfig
from meetings.models import Meeting
from meetings.tables import TableMeetings


@login_required
def meetings(request):
    data = Meeting.objects.all()
    table = TableMeetings(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'meetings.html', {
        'request': request, 'table': table, 'app': 'meetings'
    })
