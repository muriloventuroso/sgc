# -*- coding: utf-8 -*-
import calendar
import datetime
import re
import string
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django_tables2.config import RequestConfig
from django_tables2 import Column
from meetings.helpers import DesignationsSheetPdf
from meetings.models import (
    Designations, Meeting, MidweekContent, TreasuresContent, ApplyYourselfContent, LivingChristiansContent, MeetingAudience, SpeakerOut, CountSpeech, WeekendContent)
from meetings.tables import TableMeetings, TableMeetingAudience, TableSpeakerOut, TableCountSpeech
from meetings.forms import (
    FormSearchMeeting, FormMeeting, FormDesignations, FormWeekendContent, FormMidweekContent, FormTreasuresContent,
    FormApplyYourselfContent, FormLivingChristiansContent, FormGeneratePDF, FormMeetingAudience,
    FormSearchMeetingAudience, FormSpeakerOut, FormSearchSpeakerOut)
from congregations.models import Congregation, Group, Publisher
from sgc import settings
from sgc.helpers import redirect_with_next
from bson.objectid import ObjectId


@login_required
def meetings(request):
    form = FormSearchMeeting(request.GET)
    filter_m = {}
    if form.is_valid():
        data = form.cleaned_data
        if data.get('start_date'):
            filter_m['date__gte'] = data['start_date']
        else:
            filter_m['date__gte'] = datetime.datetime.now()
        if data.get('end_date'):
            filter_m['date__lte'] = data['end_date']
        if 'type_meeting' in data and data['type_meeting']:
            filter_m['type_meeting'] = data['type_meeting']
    if not request.user.is_staff:
        filter_m['congregation_id'] = request.user.congregation_id
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
    congregation_id = request.user.congregation_id
    initital = {'congregation': congregation_id}
    if request.method == 'POST':
        form = FormMeeting(request.POST, initial=initital)
        form_designations = FormDesignations(congregation_id, request.POST)
        form_midweekcontent = FormMidweekContent(congregation_id, request.POST)
        form_weekendcontent = FormWeekendContent(congregation_id, request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.congregation_id = congregation_id
            if form_designations.is_valid():
                meeting.designations = form_designations.save(commit=False)
                meeting.designations.soundman_id = request.POST.getlist(
                    'soundman')
                meeting.designations.attendants_id = request.POST.getlist(
                    'attendant')
                meeting.designations.mic_passers_id = request.POST.getlist(
                    'mic_passer')
                meeting.designations.zoom_id = request.POST.getlist(
                    'zoom')
            if meeting.type_meeting == 'w':
                if form_weekendcontent.is_valid():
                    meeting.weekend_content = form_weekendcontent.save(
                        commit=False)
                    count_speech = CountSpeech.objects.filter(speech__theme=meeting.weekend_content.theme)\
                        .filter(congregation_id=congregation_id).first()
                    if count_speech:
                        if meeting.date.strftime("%d/%m/%y") not in count_speech.dates:
                            count_speech.dates.append(
                                meeting.date.strftime("%d/%m/%y"))
                            count_speech.save()
            else:
                if form_midweekcontent.is_valid():
                    meeting.midweek_content = form_midweekcontent.save(
                        commit=False)
                    meeting.midweek_content.treasures = []
                    meeting.midweek_content.apply_yourself = []
                    meeting.midweek_content.living_christians = []
                    for i, title_treasure in enumerate(request.POST.getlist('title_treasure')):
                        item = TreasuresContent(
                            title_treasure=title_treasure,
                            room_treasure=request.POST.getlist(
                                'room_treasure')[i],
                            reading=True if str(request.POST.getlist(
                                'reading')[i]) == 'True' else False,
                            duration_treasure=request.POST.getlist(
                                'duration_treasure')[i]
                        )
                        if item.reading:
                            person_reading_id = request.POST.getlist('person_reading')[
                                i]
                            item.person_treasure_id = person_reading_id if person_reading_id else None
                        else:
                            person_treasure_id = request.POST.getlist(
                                'person_treasure')[i]
                            item.person_treasure_id = person_treasure_id if person_treasure_id else None
                        meeting.midweek_content.treasures.append(item)
                    for i, title_apply in enumerate(request.POST.getlist('title_apply')):
                        student_id = request.POST.getlist('student')[i]
                        assistant_id = request.POST.getlist('assistant')[i]
                        item = ApplyYourselfContent(
                            title_apply=title_apply,
                            room_apply=request.POST.getlist('room_apply')[i],
                            duration_apply=request.POST.getlist(
                                'duration_apply')[i],
                            student_id=student_id if student_id else None,
                            assistant_id=assistant_id if assistant_id else None,
                        )

                        meeting.midweek_content.apply_yourself.append(item)
                    for i, title_living in enumerate(request.POST.getlist('title_living')):
                        reader_id = request.POST.getlist('reader')[i]
                        person_living_id = request.POST.getlist('person_living')[
                            i]
                        item = LivingChristiansContent(
                            title_living=title_living,
                            duration_living=request.POST.getlist(
                                'duration_living')[i],
                            person_living_id=person_living_id if person_living_id else None,
                            reader_id=reader_id if reader_id else None,
                        )

                        meeting.midweek_content.living_christians.append(item)

            meeting.save()
            messages.success(request, _("Meeting added successfully"))
            return redirect_with_next(request, 'meetings')

    else:
        form = FormMeeting(initial=initital)
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
        'congregation_id': congregation_id, 'range_attendants': range(request.user.congregation.n_attendants),
        'range_mic_passers': range(request.user.congregation.n_mic_passers),
        'range_soundman': range(request.user.congregation.n_soundman),
        'range_zoom': range(request.user.congregation.n_zoom),
    })


@login_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=ObjectId(meeting_id))
    meeting.date = meeting.date.strftime('%d/%m/%Y')
    congregation_id = meeting.congregation_id
    initital = {'congregation': congregation_id}
    if request.method == 'POST':
        form = FormMeeting(request.POST, instance=meeting, initial=initital)
        form_designations = FormDesignations(congregation_id, request.POST)
        form_weekendcontent = FormWeekendContent(congregation_id, request.POST)
        form_midweekcontent = FormMidweekContent(congregation_id, request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.congregation_id = congregation_id
            if form_designations.is_valid():
                meeting.designations = form_designations.save(commit=False)
                meeting.designations.soundman_id = request.POST.getlist(
                    'soundman')
                meeting.designations.attendants_id = request.POST.getlist(
                    'attendant')
                meeting.designations.mic_passers_id = request.POST.getlist(
                    'mic_passer')
                meeting.designations.zoom_id = request.POST.getlist(
                    'zoom')
            if meeting.type_meeting == 'w':
                if form_weekendcontent.is_valid():
                    old_theme = meeting.weekend_content.theme
                    meeting.weekend_content = form_weekendcontent.save(
                        commit=False)
                    if old_theme != meeting.weekend_content.theme:
                        count_speech = CountSpeech.objects.filter(speech__theme=old_theme)\
                            .filter(congregation_id=congregation_id).first()
                        if count_speech:
                            if meeting.date.strftime("%d/%m/%y") in count_speech.dates:
                                count_speech.dates.remove(
                                    meeting.date.strftime("%d/%m/%y"))
                                count_speech.save()
                    count_speech = CountSpeech.objects.filter(speech__theme=meeting.weekend_content.theme)\
                        .filter(congregation_id=congregation_id).first()
                    if count_speech:
                        if meeting.date.strftime("%d/%m/%y") not in count_speech.dates:
                            count_speech.dates.append(
                                meeting.date.strftime("%d/%m/%y"))
                            count_speech.save()
            else:
                if form_midweekcontent.is_valid():
                    meeting.midweek_content = form_midweekcontent.save(
                        commit=False)
                    meeting.midweek_content.treasures = []
                    meeting.midweek_content.apply_yourself = []
                    meeting.midweek_content.living_christians = []
                    for i, title_treasure in enumerate(request.POST.getlist('title_treasure')):
                        item = TreasuresContent(
                            title_treasure=title_treasure,
                            room_treasure=request.POST.getlist(
                                'room_treasure')[i],
                            reading=True if str(request.POST.getlist(
                                'reading')[i]) == 'True' else False,
                            duration_treasure=request.POST.getlist(
                                'duration_treasure')[i]
                        )
                        if item.reading:
                            person_reading_id = request.POST.getlist('person_reading')[
                                i]
                            item.person_treasure_id = person_reading_id if person_reading_id else None
                        else:
                            person_treasure_id = request.POST.getlist(
                                'person_treasure')[i]
                            item.person_treasure_id = person_treasure_id if person_treasure_id else None
                        meeting.midweek_content.treasures.append(item)
                    for i, title_apply in enumerate(request.POST.getlist('title_apply')):
                        student_id = request.POST.getlist('student')[i]
                        assistant_id = request.POST.getlist('assistant')[i]
                        item = ApplyYourselfContent(
                            title_apply=title_apply,
                            room_apply=request.POST.getlist('room_apply')[i],
                            duration_apply=request.POST.getlist(
                                'duration_apply')[i],
                            student_id=student_id if student_id else None,
                            assistant_id=assistant_id if assistant_id else None,
                        )

                        meeting.midweek_content.apply_yourself.append(item)
                    for i, title_living in enumerate(request.POST.getlist('title_living')):
                        reader_id = request.POST.getlist('reader')[i]
                        person_living_id = request.POST.getlist('person_living')[
                            i]
                        item = LivingChristiansContent(
                            title_living=title_living,
                            duration_living=request.POST.getlist(
                                'duration_living')[i],
                            person_living_id=person_living_id if person_living_id else None,
                            reader_id=reader_id if reader_id else None,
                        )

                        meeting.midweek_content.living_christians.append(item)

            meeting.save()
            messages.success(request, _("Meeting edited successfully"))
            return redirect_with_next(request, 'meetings')
    else:
        form = FormMeeting(instance=meeting)
        form_designations = FormDesignations(
            congregation_id, instance=meeting.designations)
        form_weekendcontent = FormWeekendContent(
            congregation_id, instance=meeting.weekend_content)
        form_midweekcontent = FormMidweekContent(
            congregation_id, instance=meeting.midweek_content)
    list_form_treasurescontent = []
    list_form_applyyourselfcontent = []
    list_form_livingchristianscontent = []
    if meeting.type_meeting == 'm':
        for f in meeting.midweek_content.treasures:
            initial = {}
            if f.reading and f.person_treasure_id:
                initial['person_reading'] = f.person_treasure
            list_form_treasurescontent.append(FormTreasuresContent(
                congregation_id, instance=f, initial=initial))
        for f in meeting.midweek_content.apply_yourself:
            list_form_applyyourselfcontent.append(
                FormApplyYourselfContent(congregation_id, instance=f))
        for f in meeting.midweek_content.living_christians:
            list_form_livingchristianscontent.append(
                FormLivingChristiansContent(congregation_id, instance=f))
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
        'list_form_livingchristianscontent': list_form_livingchristianscontent,
        'range_attendants': range(request.user.congregation.n_attendants),
        'range_mic_passers': range(request.user.congregation.n_mic_passers),
        'range_soundman': range(request.user.congregation.n_soundman),
        'range_zoom': range(request.user.congregation.n_zoom),
        'meeting': meeting
    })


@login_required
def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=ObjectId(meeting_id))
    meeting.delete()
    messages.success(request, _("Meeting deleted successfully"))
    return redirect('meetings')


@login_required
def generate_pdf(request):
    from weasyprint import HTML, CSS
    
    from meetings.helpers import get_page_body
    if request.method == 'POST':
        form = FormGeneratePDF(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            filter_m = {'congregation_id': request.user.congregation_id}
            if data['type_pdf'] == "s":
                filter_m['type_meeting'] = 'm'
                meetings = Meeting.objects.filter(date__gte=data['start_date'], date__lt=data['end_date']).filter(**filter_m)\
                    .order_by('date')
                s89 = DesignationsSheetPdf(meetings)
                s89.generate()
                pdf_file = s89.save()

                response = HttpResponse(
                    pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="' + \
                    's89.pdf"'
                return response
            else:
                rooms = 1
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
                meetings = Meeting.objects.filter(date__gte=data['start_date'], date__lt=data['end_date']).filter(**filter_m)\
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
                if data['type_pdf'] == 'w':
                    context['speakers_out'] = SpeakerOut.objects.filter(date__range=[data['start_date'], data['end_date']])\
                        .filter(congregation_id=request.user.congregation_id)
                layout = render_to_string(template, context)
                html = HTML(string=layout)
                main_doc = html.render(stylesheets=[CSS('static/css/pdf.css')])
                html = HTML(string=render_to_string(template_header))
                header = html.render(stylesheets=[CSS('static/css/pdf.css')])
                header_page = header.pages[0]
                header_body = get_page_body(header_page._page_box.all_children())
                header_body = header_body.copy_with_children(
                    header_body.all_children())
                for i, page in enumerate(main_doc.pages):
                    page_body = get_page_body(page._page_box.all_children())
                    page_body.children += header_body.all_children()
                pdf_file = main_doc.write_pdf()
                response = HttpResponse(pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="report.pdf"'
                return response
    else:
        form = FormGeneratePDF()
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
        return HttpResponse(status=400)
    date = datetime.datetime.strptime(request.GET['date'], '%d/%m/%Y')
    filter_m['date__lte'] = date

    if 'type' not in request.GET or not request.GET['type']:
        return HttpResponse(status=400)

    if 'congregation_id' not in request.GET or not request.GET['congregation_id']:
        congregation_id = request.user.congregation_id
    else:
        congregation_id = request.GET['congregation_id']
    filter_m['congregation_id'] = congregation_id
    meetings = Meeting.objects.filter(**filter_m).order_by('-date')
    if request.GET['type'] == 'soundman':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['soundman'], congregation_id=congregation_id)]
        for meeting in meetings:
            if (
                    meeting.designations.soundman_id and str(
                        meeting.designations.soundman_id)
                    not in list_publishers_meetings):
                list_publishers_meetings.append(
                    str(meeting.designations.soundman_id))
    elif request.GET['type'] == 'attendant':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['attendant'], congregation_id=congregation_id)]
        for meeting in meetings:
            if not meeting.designations.attendants_id:
                continue
            for attendant_id in meeting.designations.attendants_id:
                if attendant_id and str(attendant_id) not in list_publishers_meetings:
                    list_publishers_meetings.append(str(attendant_id))
    elif request.GET['type'] == 'mic_passer':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['mic_passer'], congregation_id=congregation_id)]
        for meeting in meetings:
            if not meeting.designations.mic_passers_id:
                continue
            for mic_passer_id in meeting.designations.mic_passers_id:
                if mic_passer_id and str(mic_passer_id) not in list_publishers_meetings:
                    list_publishers_meetings.append(str(mic_passer_id))
    elif request.GET['type'] == 'zoom':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['zoom'], congregation_id=congregation_id)]
        for meeting in meetings:
            if not meeting.designations.zoom_id:
                continue
            for zoom_id in meeting.designations.zoom_id:
                if zoom_id and str(zoom_id) not in list_publishers_meetings:
                    list_publishers_meetings.append(str(zoom_id))
    elif request.GET['type'] == 'stage':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['stage'], congregation_id=congregation_id)]
        for meeting in meetings:
            if meeting.designations.stage_id and str(meeting.designations.stage_id) not in list_publishers_meetings:
                list_publishers_meetings.append(
                    str(meeting.designations.stage_id))
    elif request.GET['type'] == 'reader_w':
        list_publishers = [
            (str(p._id), p.full_name) for p in Publisher.objects.filter(
                tags__in=['reader_w'], congregation_id=congregation_id)]
        for meeting in meetings:
            if meeting.type_meeting == 'm':
                continue
            if (
                    meeting.weekend_content.reader_id and str(
                        meeting.weekend_content.reader_id)
                    not in list_publishers_meetings):
                list_publishers_meetings.append(
                    str(meeting.weekend_content.reader_id))
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

    congregation = request.user.congregation

    date = datetime.datetime.strptime(request.GET['date'], '%d/%m/%Y')
    url = settings.URL_JW_MEETINGS_PT + date.strftime('%Y/%m/%d')
    code = requests.get(url)
    plain = code.text
    plain = plain.replace('\xa0', ' ')
    s = BeautifulSoup(plain, "html.parser")
    reading_week = s.find('h2', {'id': 'p2'}).text.capitalize()
    first_song = s.find('p', {'id': 'p3'}).find('a').text.split(' ')[1]
    second_song = s.find('div', {'id': 'section4'}).findAll('li')[
        0].find('a').text.split(' ')[1]
    third_song = s.find('div', {'id': 'section4'}).findAll(
        'li')[-1].find('a').text.split(' ')[1]
    treasures = []
    for t in s.find('div', {'id': 'section2'}).findAll('p', {'class': 'so'}):
        duration = re.search(r'\(([0-9].*\))', t.text).group(1).split(")")[0]
        try:
            title = t.text[:t.text.index(duration)].strip().rstrip(
                ",.:('").strip().rstrip(",.:('")
            if 'Leitura' in title:
                n_rooms = congregation.n_rooms
                reading = True
            else:
                reading = False
                n_rooms = 1
            for i in range(n_rooms):
                treasures.append({
                    'title': t.text[:t.text.index(duration)].strip().rstrip(",.:('").strip().rstrip(",.:('"),
                    'duration': duration,
                    'room': list(string.ascii_lowercase)[i].upper(),
                    'reading': reading
                })
        except Exception:
            pass

    apply_yourself = []
    for a in s.find('div', {'id': 'section3'}).findAll('p', {'class': 'so'}):
        duration = re.search(r'\(([0-9].*\))', a.text).group(1).split(")")[0]
        try:
            for i in range(congregation.n_rooms):
                apply_yourself.append({
                    'title': a.text[:a.text.index(duration)].strip().rstrip(",.:('").strip().rstrip(",.:('"),
                    'duration': duration,
                    'room': list(string.ascii_lowercase)[i].upper()
                })
        except Exception:
            pass
    living_christians = []
    for l in s.find('div', {'id': 'section4'}).findAll('p', {'class': 'so'})[1:-2]:
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
    form = FormSearchMeetingAudience(request.GET)
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
        filter_data['congregation_id'] = request.user.congregation_id
    data = MeetingAudience.objects.filter(**filter_data)
    table = TableMeetingAudience(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'meeting_audiences.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'meetings', 'page_title': _("Meeting Audiences"),
        'next': request.GET.copy().urlencode()
    })


def add_meeting_audience(request):
    if request.user.is_authenticated:
        congregation_id = request.user.congregation_id
    else:
        if 'congregation_id' in request.GET and request.GET['congregation_id']:
            congregation_id = request.GET['congregation_id']
        else:
            return HttpResponse(status=401)
    if request.method == 'POST':
        form = FormMeetingAudience(request.POST)
        if form.is_valid():
            meeting_audience = form.save(commit=False)
            for i, absence in enumerate(request.POST.getlist('absences')):
                meeting_audience.absences.add(
                    Publisher.objects.get(pk=ObjectId(absence)))
            meeting_audience.congregation_id = congregation_id
            meeting_audience.save()
            messages.success(request, _("Meeting Audience added successfully"))
            return redirect_with_next(request, 'meeting_audiences')
    else:
        form = FormMeetingAudience()
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
    meeting_audience = get_object_or_404(
        MeetingAudience, pk=ObjectId(meeting_audience_id))
    if request.method == 'POST':
        form = FormMeetingAudience(request.POST, instance=meeting_audience)
        if form.is_valid():
            meeting_audience = form.save(commit=False)
            meeting_audience.absences.clear()
            for i, absence in enumerate(request.POST.getlist('absences')):
                meeting_audience.absences.add(
                    Publisher.objects.get(pk=ObjectId(absence)))
            meeting_audience.save()
            messages.success(request, _(
                "Meeting Audience edited successfully"))
            return redirect_with_next(request, 'meeting_audiences')
    else:
        form = FormMeetingAudience(instance=meeting_audience)
    checked_publishers = [
        x.pk for x in meeting_audience.absences.get_queryset()]
    all_publishers = Publisher.objects.filter(
        congregation_id=meeting_audience.congregation_id)
    return render(request, 'add_edit_meeting_audience.html', {
        'request': request, 'form': form, 'page_group': 'meetings', 'page_title': _("Edit Meeting Audience"),
        'checked_publishers': checked_publishers, 'all_publishers': all_publishers
    })


@login_required
def delete_meeting_audience(request, meeting_audience_id):
    meeting_audience = get_object_or_404(
        MeetingAudience, pk=ObjectId(meeting_audience_id))
    meeting_audience.delete()
    messages.success(request, _("Meeting Audience deleted successfully"))
    return redirect_with_next(request, 'meeting_audiences')


@login_required
def speakers_out(request):
    form = FormSearchSpeakerOut(request.GET)
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
        filter_data['congregation_id'] = request.user.congregation_id
    data = SpeakerOut.objects.filter(**filter_data)
    table = TableSpeakerOut(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'speakers_out.html', {
        'request': request, 'table': table, 'form': form,
        'page_group': 'meetings', 'page_title': _("Speakers Out"),
        'next': request.GET.copy().urlencode()
    })


@login_required
def add_speaker_out(request):
    congregation_id = request.user.congregation_id

    if request.method == 'POST':
        form = FormSpeakerOut(request.user.congregation_id, request.POST)
        if form.is_valid():
            speaker_out = form.save(commit=False)
            speaker_out.congregation_id = congregation_id
            speaker_out.save()
            messages.success(request, _("Speaker Out added successfully"))
            return redirect_with_next(request, 'speakers_out')
    else:
        form = FormSpeakerOut(request.user.congregation_id)

    return render(request, 'add_edit_speaker_out.html', {
        'request': request, 'form': form, 'page_group': 'meetings', 'page_title': _("Add Speaker Out"),
    })


@login_required
def edit_speaker_out(request, speaker_out_id):
    speaker_out = get_object_or_404(SpeakerOut, pk=ObjectId(speaker_out_id))
    if request.method == 'POST':
        form = FormSpeakerOut(
            request.user.congregation_id, request.POST, instance=speaker_out)
        if form.is_valid():
            speaker_out = form.save()
            messages.success(request, _("Speaker Out edited successfully"))
            return redirect_with_next(request, 'speakers_out')
    else:
        form = FormSpeakerOut(request.user.congregation_id,
                              instance=speaker_out)
    return render(request, 'add_edit_speaker_out.html', {
        'request': request, 'form': form, 'page_group': 'meetings', 'page_title': _("Edit Speaker Out"),
    })


@login_required
def delete_speaker_out(request, speaker_out_id):
    speaker_out = get_object_or_404(SpeakerOut, pk=ObjectId(speaker_out_id))
    speaker_out.delete()
    messages.success(request, _("Speaker Out deleted successfully"))
    return redirect_with_next(request, 'speakers_out')


@login_required
def speeches(request):
    data_db = CountSpeech.objects.filter(congregation_id=request.user.congregation_id).select_related('speech')\
        .order_by('speech__number')
    data = []
    date_keys = []
    extra_columns = []
    for d in data_db:
        item = {
            'speech': d.speech
        }
        for d in d.dates:
            date = datetime.datetime.strptime(d, '%d/%m/%y')
            year = str(date.year)
            if year not in date_keys:
                date_keys.append(year)
            if year not in item:
                item[year] = ""
            item[year] += date.strftime('%d/%m') + ', '
        data.append(item)
    for d in data:
        for key, value in d.items():
            if key != 'speech':
                if value.endswith(', '):
                    d[key] = value[:-2]
    for key in sorted(date_keys):
        extra_columns.append((key, Column(verbose_name=key)))
    table = TableCountSpeech(data, extra_columns=extra_columns)
    return render(request, 'speeches.html', {
        'request': request, 'table': table,
        'page_group': 'meetings', 'page_title': _("Speeches"),
        'next': request.GET.copy().urlencode()
    })


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

        layout = render_to_string(template, context)
    elif type_board == 'groups':
        template = 'pdf/groups.html'
        title = _("Groups")
        groups = Group.objects.filter(congregation_id=congregation._id).order_by('name')
    return render(request, 'bulletin_board.html', {
        'request': request, 'layout': layout, 'congregation_id': congregation_id, 'type_board': type_board,
        'page_group': 'meetings', 'page_title': _("Bulletin Board"), 'title': title,
        'next': request.GET.copy().urlencode()
    })