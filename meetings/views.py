# -*- coding: utf-8 -*-
import datetime
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django_tables2.config import RequestConfig
from meetings.models import Meeting, TreasuresContent, ApplyYourselfContent, LivingChristiansContent, MeetingAudience
from meetings.tables import TableMeetings, TableMeetingAudience
from meetings.forms import (
    FormSearchMeeting, FormMeeting, FormDesignations, FormWeekendContent, FormMidweekContent, FormTreasuresContent,
    FormApplyYourselfContent, FormLivingChristiansContent, FormGeneratePDF, FormMeetingAudience,
    FormSearchMeetingAudience)
from congregations.models import Publisher
from users.models import UserProfile
from sgc import settings
from sgc.helpers import redirect_with_next


@login_required
def meetings(request):
    profile = UserProfile.objects.get(user=request.user)
    form = FormSearchMeeting(request.LANGUAGE_CODE, request.GET)
    filter_m = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'start_date' in data and data['start_date']:
            filter_m['date__gte'] = data['start_date']
        else:
            filter_m['date__gte'] = datetime.datetime.now()
        if 'end_date' in data and data['end_date']:
            filter_m['date__lte'] = data['end_date']
        if 'type_meeting' in data and data['type_meeting']:
            filter_m['type_meeting'] = data['type_meeting']
    if not request.user.is_staff:
        filter_m['congregation_id'] = profile.congregation_id
    data = Meeting.objects.filter(**filter_m)
    table = TableMeetings(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'meetings.html', {
        'request': request, 'table': table, 'page_group': 'meetings',
        'page_title': _("Meetings"), 'form': form,
        'next': request.GET.copy().urlencode()
    })


@login_required
def add_meeting(request):
    profile = UserProfile.objects.get(user=request.user)
    congregation_id = profile.congregation_id
    initital = {'congregation': congregation_id}
    if request.method == 'POST':
        form = FormMeeting(profile, request.LANGUAGE_CODE, request.POST, initial=initital)
        form_designations = FormDesignations(congregation_id, request.POST)
        form_midweekcontent = FormMidweekContent(congregation_id, request.POST)
        form_weekendcontent = FormWeekendContent(congregation_id, request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.congregation_id = congregation_id
            if form_designations.is_valid():
                meeting.designations = form_designations.save(commit=False)
            if meeting.type_meeting == 'w':
                if form_weekendcontent.is_valid():
                    meeting.weekend_content = form_weekendcontent.save(commit=False)
            else:
                if form_midweekcontent.is_valid():
                    meeting.midweek_content = form_midweekcontent.save(commit=False)
                    meeting.midweek_content.treasures = []
                    meeting.midweek_content.apply_yourself = []
                    meeting.midweek_content.living_christians = []
                    for i, title_treasure in enumerate(request.POST.getlist('title_treasure')):
                        item = TreasuresContent(
                            title_treasure=title_treasure,
                            room_treasure=request.POST.getlist('room_treasure')[i],
                            reading=True if str(request.POST.getlist('reading')[i]) == 'True' else False,
                            duration_treasure=request.POST.getlist('duration_treasure')[i]
                        )
                        if item.reading:
                            person_reading_id = request.POST.getlist('person_reading')[i]
                            item.person_treasure_id = person_reading_id if person_reading_id else None
                        else:
                            person_treasure_id = request.POST.getlist('person_treasure')[i]
                            item.person_treasure_id = person_treasure_id if person_treasure_id else None
                        meeting.midweek_content.treasures.append(item)
                    for i, title_apply in enumerate(request.POST.getlist('title_apply')):
                        student_id = request.POST.getlist('student')[i]
                        assistant_id = request.POST.getlist('assistant')[i]
                        item = ApplyYourselfContent(
                            title_apply=title_apply,
                            room_apply=request.POST.getlist('room_apply')[i],
                            duration_apply=request.POST.getlist('duration_apply')[i],
                            student_id=student_id if student_id else None,
                            assistant_id=assistant_id if assistant_id else None,
                        )

                        meeting.midweek_content.apply_yourself.append(item)
                    for i, title_living in enumerate(request.POST.getlist('title_living')):
                        reader_id = request.POST.getlist('reader')[i]
                        person_living_id = request.POST.getlist('person_living')[i]
                        item = LivingChristiansContent(
                            title_living=title_living,
                            duration_living=request.POST.getlist('duration_living')[i],
                            person_living_id=person_living_id if person_living_id else None,
                            reader_id=reader_id if reader_id else None,
                        )

                        meeting.midweek_content.living_christians.append(item)

            meeting.save()
            messages.success(request, _("Meeting added successfully"))
            return redirect_with_next(request, 'meetings')

    else:
        form = FormMeeting(profile, request.LANGUAGE_CODE, initial=initital)
        form_designations = FormDesignations(congregation_id)
        form_weekendcontent = FormWeekendContent(congregation_id)
        form_midweekcontent = FormMidweekContent(congregation_id)
    form_treasurescontent = FormTreasuresContent(congregation_id)
    form_applyyourselfcontent = FormApplyYourselfContent(congregation_id)
    form_livingchristianscontent = FormLivingChristiansContent(congregation_id)
    return render(request, 'add_meeting.html', {
        'request': request, 'form': form, 'page_group': 'meetings', 'page_title': _("Add Meeting"),
        'form_designations': form_designations, 'form_weekendcontent': form_weekendcontent,
        'form_midweekcontent': form_midweekcontent, 'form_treasurescontent': form_treasurescontent,
        'form_applyyourselfcontent': form_applyyourselfcontent,
        'form_livingchristianscontent': form_livingchristianscontent,
        'congregation_id': congregation_id
    })


@login_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    profile = UserProfile.objects.get(user=request.user)
    meeting.date = meeting.date.strftime('%d/%m/%Y')
    congregation_id = meeting.congregation_id
    initital = {'congregation': congregation_id}
    if request.method == 'POST':
        form = FormMeeting(profile, request.LANGUAGE_CODE, request.POST, instance=meeting, initial=initital)
        form_designations = FormDesignations(congregation_id, request.POST)
        form_weekendcontent = FormWeekendContent(congregation_id, request.POST)
        form_midweekcontent = FormMidweekContent(congregation_id, request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.congregation_id = congregation_id
            if form_designations.is_valid():
                meeting.designations = form_designations.save(commit=False)
            if meeting.type_meeting == 'w':
                if form_weekendcontent.is_valid():
                    meeting.weekend_content = form_weekendcontent.save(commit=False)
            else:
                if form_midweekcontent.is_valid():
                    meeting.midweek_content = form_midweekcontent.save(commit=False)
                    meeting.midweek_content.treasures = []
                    meeting.midweek_content.apply_yourself = []
                    meeting.midweek_content.living_christians = []
                    for i, title_treasure in enumerate(request.POST.getlist('title_treasure')):
                        item = TreasuresContent(
                            title_treasure=title_treasure,
                            room_treasure=request.POST.getlist('room_treasure')[i],
                            reading=True if str(request.POST.getlist('reading')[i]) == 'True' else False,
                            duration_treasure=request.POST.getlist('duration_treasure')[i]
                        )
                        if item.reading:
                            person_reading_id = request.POST.getlist('person_reading')[i]
                            item.person_treasure_id = person_reading_id if person_reading_id else None
                        else:
                            person_treasure_id = request.POST.getlist('person_treasure')[i]
                            item.person_treasure_id = person_treasure_id if person_treasure_id else None
                        meeting.midweek_content.treasures.append(item)
                    for i, title_apply in enumerate(request.POST.getlist('title_apply')):
                        student_id = request.POST.getlist('student')[i]
                        assistant_id = request.POST.getlist('assistant')[i]
                        item = ApplyYourselfContent(
                            title_apply=title_apply,
                            room_apply=request.POST.getlist('room_apply')[i],
                            duration_apply=request.POST.getlist('duration_apply')[i],
                            student_id=student_id if student_id else None,
                            assistant_id=assistant_id if assistant_id else None,
                        )

                        meeting.midweek_content.apply_yourself.append(item)
                    for i, title_living in enumerate(request.POST.getlist('title_living')):
                        reader_id = request.POST.getlist('reader')[i]
                        person_living_id = request.POST.getlist('person_living')[i]
                        item = LivingChristiansContent(
                            title_living=title_living,
                            duration_living=request.POST.getlist('duration_living')[i],
                            person_living_id=person_living_id if person_living_id else None,
                            reader_id=reader_id if reader_id else None,
                        )

                        meeting.midweek_content.living_christians.append(item)

            meeting.save()
            messages.success(request, _("Meeting edited successfully"))
            return redirect_with_next(request, 'meetings')
    else:
        form = FormMeeting(profile, request.LANGUAGE_CODE, instance=meeting)
        form_designations = FormDesignations(congregation_id, instance=meeting.designations)
        form_weekendcontent = FormWeekendContent(congregation_id, instance=meeting.weekend_content)
        form_midweekcontent = FormMidweekContent(congregation_id, instance=meeting.midweek_content)
    list_form_treasurescontent = []
    list_form_applyyourselfcontent = []
    list_form_livingchristianscontent = []
    if meeting.type_meeting == 'm':
        for f in meeting.midweek_content.treasures:
            initial = {}
            if f.reading and f.person_treasure_id:
                initial['person_reading'] = f.person_treasure
            list_form_treasurescontent.append(FormTreasuresContent(congregation_id, instance=f, initial=initial))
        for f in meeting.midweek_content.apply_yourself:
            list_form_applyyourselfcontent.append(FormApplyYourselfContent(congregation_id, instance=f))
        for f in meeting.midweek_content.living_christians:
            list_form_livingchristianscontent.append(FormLivingChristiansContent(congregation_id, instance=f))
    form_treasurescontent = FormTreasuresContent(congregation_id)
    form_applyyourselfcontent = FormApplyYourselfContent(congregation_id)
    form_livingchristianscontent = FormLivingChristiansContent(congregation_id)
    return render(request, 'edit_meeting.html', {
        'request': request, 'form': form, 'page_group': 'meetings', 'page_title': _("Edit Meeting"),
        'form_designations': form_designations, 'form_weekendcontent': form_weekendcontent,
        'form_midweekcontent': form_midweekcontent, 'form_treasurescontent': form_treasurescontent,
        'form_applyyourselfcontent': form_applyyourselfcontent,
        'form_livingchristianscontent': form_livingchristianscontent,
        'list_form_treasurescontent': list_form_treasurescontent,
        'list_form_applyyourselfcontent': list_form_applyyourselfcontent,
        'list_form_livingchristianscontent': list_form_livingchristianscontent
    })


@login_required
def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    meeting.delete()
    messages.success(request, _("Meeting deleted successfully"))
    return redirect('meetings')


@login_required
def generate_pdf(request):
    from weasyprint import HTML, CSS
    from django.template.loader import render_to_string
    from django.http import HttpResponse
    from meetings.helpers import get_page_body
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FormGeneratePDF(request.LANGUAGE_CODE, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            filter_m = {'congregation_id': profile.congregation_id}
            if data['type_pdf'] == 'd':
                template = 'pdf/designations.html'
                template_header = 'pdf/header_designations.html'
            elif data['type_pdf'] == 'w':
                template = 'pdf/weekend.html'
                template_header = 'pdf/header_weekend.html'
                filter_m['type_meeting'] = 'w'
            elif data['type_pdf'] == 'm':
                template = 'pdf/midweek.html'
                template_header = 'pdf/header_midweek.html'
                filter_m['type_meeting'] = 'm'
            meetings = Meeting.objects.filter(date__range=[data['start_date'], data['end_date']]).filter(**filter_m)\
                .order_by('date')
            layout = render_to_string(template, {'meetings': meetings})
            html = HTML(string=layout)
            main_doc = html.render(stylesheets=[CSS('static/css/pdf.css')])

            html = HTML(string=render_to_string(template_header))
            header = html.render(stylesheets=[CSS('static/css/pdf.css')])
            header_page = header.pages[0]
            header_body = get_page_body(header_page._page_box.all_children())
            header_body = header_body.copy_with_children(header_body.all_children())

            for i, page in enumerate(main_doc.pages):
                page_body = get_page_body(page._page_box.all_children())
                page_body.children += header_body.all_children()

            pdf_file = main_doc.write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            return response
    else:
        form = FormGeneratePDF(request.LANGUAGE_CODE)
    return render(request, 'generate_pdf.html', {
        'request': request, 'form': form, 'page_group': 'meetings', 'page_title': _("Generate PDF"),
    })


@login_required
def suggest_publisher(request):
    ret = []
    filter_m = {}
    list_publishers_meetings = []
    list_publishers = []
    if 'date' not in request.GET or not request.GET['date']:
        return HttpResponse(status=401)
    date = datetime.datetime.strptime(request.GET['date'], '%d/%m/%Y')
    filter_m['date__lte'] = date

    if 'type' not in request.GET or not request.GET['type']:
        return HttpResponse(status=401)

    if 'congregation_id' not in request.GET or not request.GET['congregation_id']:
        return HttpResponse(status=401)
    congregation_id = request.GET['congregation_id']
    filter_m['congregation_id'] = congregation_id
    meetings = Meeting.objects.filter(**filter_m).order_by('-date')
    if request.GET['type'] == 'soundman':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['soundman'], congregation_id=congregation_id)]
        for meeting in meetings:
            if (
                    meeting.designations.soundman_id and str(meeting.designations.soundman_id)
                    not in list_publishers_meetings):
                list_publishers_meetings.append(str(meeting.designations.soundman_id))
    elif request.GET['type'] == 'attendant1' or request.GET['type'] == 'attendant2':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['attendant'], congregation_id=congregation_id)]
        for meeting in meetings:
            if (
                    meeting.designations.attendant1_id and str(meeting.designations.attendant1_id)
                    not in list_publishers_meetings):
                list_publishers_meetings.append(str(meeting.designations.attendant1_id))
            if (
                    meeting.designations.attendant2_id and str(meeting.designations.attendant2_id)
                    not in list_publishers_meetings):
                list_publishers_meetings.append(str(meeting.designations.attendant2_id))
    elif request.GET['type'] == 'mic_passer1' or request.GET['type'] == 'mic_passer2':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['mic_passer'], congregation_id=congregation_id)]
        for meeting in meetings:
            if (
                    meeting.designations.mic_passer1_id and str(meeting.designations.mic_passer1_id)
                    not in list_publishers_meetings):
                list_publishers_meetings.append(str(meeting.designations.mic_passer1_id))
            if (
                    meeting.designations.mic_passer2_id and str(meeting.designations.mic_passer2_id)
                    not in list_publishers_meetings):
                list_publishers_meetings.append(str(meeting.designations.mic_passer2_id))
    elif request.GET['type'] == 'stage':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['stage'], congregation_id=congregation_id)]
        for meeting in meetings:
            if meeting.designations.stage_id and str(meeting.designations.stage_id) not in list_publishers_meetings:
                list_publishers_meetings.append(str(meeting.designations.stage_id))
    elif request.GET['type'] == 'reader_w':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['reader_w'], congregation_id=congregation_id)]
        for meeting in meetings:
            if meeting.type_meeting == 'm':
                continue
            if (
                    meeting.weekend_content.reader_id and str(meeting.weekend_content.reader_id)
                    not in list_publishers_meetings):
                list_publishers_meetings.append(str(meeting.weekend_content.reader_id))
    elif request.GET['type'] == 'reader_m':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['reader_m'], congregation_id=congregation_id)]
        for meeting in meetings:
            if meeting.type_meeting == 'w':
                continue
            for living in meeting.midweek_content.living_christians:
                if living.reader_id and str(living.reader_id) not in list_publishers_meetings:
                    list_publishers_meetings.append(str(living.reader_id))
    for p in list_publishers:
        try:
            index = list_publishers_meetings.index(p[0])
        except ValueError:
            index = -1
        if index == -1:
            list_publishers_meetings.append((p[0], p[1]))
        else:
            list_publishers_meetings[index] = (p[0], p[1])
    for l in list_publishers_meetings:
        if isinstance(l, tuple):
            ret.append(l)

    return JsonResponse(list(reversed(ret)), safe=False)


@login_required
def suggest_meeting(request):
    import requests
    from bs4 import BeautifulSoup
    ret = {}

    if 'date' not in request.GET or not request.GET['date']:
        return HttpResponse(status=401)

    if 'type' not in request.GET or not request.GET['type']:
        return HttpResponse(status=401)

    if request.GET['type'] != 'midweek':
        return HttpResponse(status=401)

    date = datetime.datetime.strptime(request.GET['date'], '%d/%m/%Y')
    url = settings.URL_JW_MEETINGS_PT + date.strftime('%Y/%m/%d')
    code = requests.get(url)
    plain = code.text
    plain = plain.replace('\xa0', ' ')
    s = BeautifulSoup(plain, "html.parser")
    reading_week = s.find('h2', {'id': 'p2'}).text.capitalize()
    first_song = s.find('p', {'id': 'p3'}).find('a').text.split(' ')[1]
    second_song = s.find('div', {'id': 'section4'}).findAll('li')[0].find('a').text.split(' ')[1]
    third_song = s.find('div', {'id': 'section4'}).findAll('li')[-1].find('a').text.split(' ')[1]
    treasures = []
    for t in s.find('div', {'id': 'section2'}).findAll('p', {'class': 'su'}):
        duration = re.search(r'\(([0-9].*\))', t.text).group(1).split(")")[0]
        try:
            treasures.append({
                'title': t.text[:t.text.index(duration)].strip().rstrip(",.:('").strip().rstrip(",.:('"),
                'duration': duration
            })
        except Exception:
            pass

    apply_yourself = []
    for a in s.find('div', {'id': 'section3'}).findAll('p', {'class': 'su'}):
        duration = re.search(r'\(([0-9].*\))', a.text).group(1).split(")")[0]
        try:
            apply_yourself.append({
                'title': a.text[:a.text.index(duration)].strip().rstrip(",.:('").strip().rstrip(",.:('"),
                'duration': duration
            })
        except Exception:
            pass
    living_christians = []
    for l in s.find('div', {'id': 'section4'}).findAll('p', {'class': 'su'})[1:-2]:
        duration = re.search(r'\(([0-9].*\))', l.text).group(1).split(")")[0]
        try:
            living_christians.append({
                'title': l.text[:l.text.index(duration)].strip().rstrip(",.(:'").strip().rstrip(",.:('"),
                'duration': duration
            })
        except Exception:
            pass

    ret = {
        'reading_week': reading_week.title(),
        'first_song': first_song,
        'second_song': second_song,
        'third_song': third_song,
        'treasures': treasures,
        'apply_yourself': apply_yourself,
        'living_christians': living_christians
    }
    return JsonResponse(ret)


@login_required
def meeting_audiences(request):
    profile = UserProfile.objects.get(user=request.user)
    form = FormSearchMeetingAudience(request.LANGUAGE_CODE, request.GET)
    filter_data = {}
    if form.is_valid():
        data = form.cleaned_data
        if 'start_date' in data and data['start_date']:
            filter_data['date__gte'] = data['start_date']
        else:
            filter_data['date__gte'] = datetime.datetime.now()
        if 'end_date' in data and data['end_date']:
            filter_data['date__lte'] = data['end_date']
    if not request.user.is_staff:
        filter_data['congregation_id'] = profile.congregation_id
    data = MeetingAudience.objects.filter(**filter_data)
    table = TableMeetingAudience(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'meeting_audiences.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'financial', 'page_title': _("Meeting Audiences"),
        'next': request.GET.copy().urlencode()
    })


def add_meeting_audience(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        congregation_id = profile.congregation_id
    else:
        if 'congregation_id' in request.GET and request.GET['congregation_id']:
            congregation_id = request.GET['congregation_id']
        else:
            return HttpResponse(status=401)
    if request.method == 'POST':
        form = FormMeetingAudience(request.LANGUAGE_CODE, request.POST)
        if form.is_valid():
            meeting_audience = form.save(commit=False)
            for i, absence in enumerate(request.POST.getlist('absences')):
                meeting_audience.absences.add(Publisher.objects.get(pk=absence))
            meeting_audience.congregation_id = congregation_id
            meeting_audience.save()
            messages.success(request, _("Meeting Audience added successfully"))
            return redirect_with_next(request, 'meeting_audiences')
    else:
        form = FormMeetingAudience(request.LANGUAGE_CODE)
    all_publishers = Publisher.objects.filter(congregation_id=congregation_id)
    if request.user.is_authenticated:
        return render(request, 'add_edit_meeting_audience.html', {
            'request': request, 'form': form, 'page_group': 'meetings', 'page_title': _("Add Meeting Audience"),
            'all_publishers': all_publishers, 'checked_publishers': []
        })
    else:
        return render(request, 'add_meeting_audience_logout.html', {
            'request': request, 'form': form, 'page_group': 'meetings', 'page_title': _("Add Meeting Audience"),
            'all_publishers': all_publishers, 'checked_publishers': []
        })


@login_required
def edit_meeting_audience(request, meeting_audience_id):
    meeting_audience = get_object_or_404(MeetingAudience, pk=meeting_audience_id)
    if request.method == 'POST':
        form = FormMeetingAudience(request.LANGUAGE_CODE, request.POST, instance=meeting_audience)
        if form.is_valid():
            meeting_audience = form.save(commit=False)
            meeting_audience.absences.clear()
            for i, absence in enumerate(request.POST.getlist('absences')):
                meeting_audience.absences.add(Publisher.objects.get(pk=absence))
            meeting_audience.save()
            messages.success(request, _("Meeting Audience edited successfully"))
            return redirect_with_next(request, 'meeting_audiences')
    else:
        form = FormMeetingAudience(request.LANGUAGE_CODE, instance=meeting_audience)
    checked_publishers = [x.pk for x in meeting_audience.absences.get_queryset()]
    all_publishers = Publisher.objects.filter(congregation_id=meeting_audience.congregation_id)
    return render(request, 'add_edit_meeting_audience.html', {
        'request': request, 'form': form, 'page_group': 'meetings', 'page_title': _("Edit Meeting Audience"),
        'checked_publishers': checked_publishers, 'all_publishers': all_publishers
    })


@login_required
def delete_meeting_audience(request, meeting_audience_id):
    meeting_audience = get_object_or_404(MeetingAudience, pk=meeting_audience_id)
    meeting_audience.delete()
    messages.success(request, _("Meeting Audience deleted successfully"))
    return redirect_with_next(request, 'meeting_audiences')
