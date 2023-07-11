import calendar
import datetime
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from congregations.models import Congregation, Group, Publisher
from meetings.models import Meeting, SpeakerOut


def bulletin_board(request, congregation_id):
    congregation = get_object_or_404(Congregation, number=congregation_id)
    if not congregation.enable_board:
        return HttpResponse()
    type_board = request.GET.get('type', 'midweek')
    filter_m = {"congregation_id": congregation._id}
    start_date = datetime.datetime.today().replace(day=1)
    end_date = datetime.datetime.today().replace(day=calendar.monthrange(start_date.year, start_date.month)[1])
    layout = ""
    title = None
    if type_board in ("midweek", "weekend", "designations"):
        rooms = 1
        if type_board == 'midweek':
            template = 'pdf/midweek.html'
            filter_m['type_meeting'] = 'm'
            title = _('Schedule of the Midweek Meeting')
        elif type_board == 'designations':
            template = 'pdf/designations.html'
            title = _("Attendants and Sound System")
        elif type_board == 'weekend':
            template = 'pdf/weekend.html'
            filter_m['type_meeting'] = 'w'
            title = _("Public Meeting and Study of Watchtower")
            
        meetings = Meeting.objects.filter(date__gte=start_date.strftime("%Y-%m-%d"), date__lt=end_date.strftime("%Y-%m-%d")).filter(**filter_m)\
            .order_by('date')
        for meeting in meetings:
            if meeting.midweek_content:
                for treasure in meeting.midweek_content.treasures:
                    if treasure.room_treasure == "B":
                        rooms = 2
                        break
                for apply_y in meeting.midweek_content.apply_yourself:
                    if apply_y.room_apply == "B":
                        rooms = 2
                        break
        context = {'meetings': meetings, 'rooms': rooms}
        if type_board == "weekend":
            context['speakers_out'] = SpeakerOut.objects.filter(congregation_id=request.user.congregation_id, date__gte=start_date.strftime("%Y-%m-%d"), date__lt=end_date.strftime("%Y-%m-%d"))


        layout = render_to_string(template, context)
    elif type_board == 'groups':
        template = 'pdf/groups.html'
        title = _("Service Groups")
        groups_data = Group.objects.filter(congregation_id=congregation._id).order_by('name')
        groups = []
        for group in groups_data:
            item = {
                'group': group,
                'publishers': []
            }
            count = 1
            if group.leader:
                count += 1
            if group.assistant:
                count += 1
            for p in Publisher.objects.filter(group_id=group._id).order_by('full_name'):
                if p != group.leader and p != group.assistant:
                    item['publishers'].append({
                        'name': str(p),
                        'count': count
                    })
                    count += 1
            groups.append(item)
        context = {'groups': groups}
        layout = render_to_string(template, context)
    elif type_board == 'agenda':
        title = _("Theocratic Agenda")
        layout = congregation.theocratic_agenda if congregation.theocratic_agenda else ""

    return render(request, 'bulletin_board.html', {
        'request': request, 'layout': layout, 'congregation_id': congregation_id, 'type_board': type_board,
        'page_group': 'meetings', 'page_title': _("Bulletin Board"), 'title': title,
        'next': request.GET.copy().urlencode()
    })