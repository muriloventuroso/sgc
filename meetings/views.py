import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django_tables2.config import RequestConfig
from meetings.models import Meeting, TreasuresContent, ApplyYourselfContent, LivingChristiansContent
from meetings.tables import TableMeetings
from meetings.forms import (
    FormSearchMeeting, FormMeeting, FormDesignations, FormWeekendContent, FormMidweekContent, FormTreasuresContent,
    FormApplyYourselfContent, FormLivingChristiansContent)


@login_required
def meetings(request):
    form = FormSearchMeeting(request.GET)
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
    data = Meeting.objects.filter(**filter_m)
    table = TableMeetings(data)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(table)
    return render(request, 'meetings.html', {
        'request': request, 'table': table, 'app': 'meetings', 'form': form
    })


@login_required
def add_meeting(request):
    if request.method == 'POST':
        form = FormMeeting(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            form_designations = FormDesignations(request.POST)
            if form_designations.is_valid():
                meeting.designations = form_designations.save(commit=False)
            if meeting.type_meeting == 'w':
                form_weekendcontent = FormWeekendContent(request.POST)
                if form_weekendcontent.is_valid():
                    meeting.weekend_content = form_weekendcontent.save(commit=False)
            else:
                print(request.POST)
                form_midweekcontent = FormMidweekContent(request.POST)
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
                            item.person_treasure_id = request.POST.getlist('person_reading')[i]
                        else:
                            item.person_treasure_id = request.POST.getlist('person_treasure')[i]
                        meeting.midweek_content.treasures.append(item)
                    for i, title_apply in enumerate(request.POST.getlist('title_apply')):
                        item = ApplyYourselfContent(
                            title_apply=title_apply,
                            room_apply=request.POST.getlist('room_apply')[i],
                            duration_apply=request.POST.getlist('duration_apply')[i],
                            student_id=request.POST.getlist('student')[i],
                            assistant_id=request.POST.getlist('assistant')[i],
                        )

                        meeting.midweek_content.apply_yourself.append(item)
                    for i, title_living in enumerate(request.POST.getlist('title_living')):
                        item = LivingChristiansContent(
                            title_living=title_living,
                            duration_living=request.POST.getlist('duration_living')[i],
                            person_living_id=request.POST.getlist('person_living')[i],
                            reader_id=request.POST.getlist('reader')[i],
                        )

                        meeting.midweek_content.living_christians.append(item)
            meeting.save()
            messages.success(request, _("Meeting added successfully"))
            return redirect('meetings')
    else:
        form = FormMeeting()
        form_designations = FormDesignations()
        form_weekendcontent = FormWeekendContent()
        form_midweekcontent = FormMidweekContent()
        form_treasurescontent = FormTreasuresContent()
        form_applyyourselfcontent = FormApplyYourselfContent()
        form_livingchristianscontent = FormLivingChristiansContent()
    return render(request, 'add_meeting.html', {
        'request': request, 'form': form, 'app': 'meetings',
        'form_designations': form_designations, 'form_weekendcontent': form_weekendcontent,
        'form_midweekcontent': form_midweekcontent, 'form_treasurescontent': form_treasurescontent,
        'form_applyyourselfcontent': form_applyyourselfcontent,
        'form_livingchristianscontent': form_livingchristianscontent
    })


@login_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    meeting.date = meeting.date.strftime('%d/%m/%Y')
    if request.method == 'POST':
        form = FormMeeting(request.POST, instance=meeting)
        if form.is_valid():
            meeting = form.save(commit=False)
            form_designations = FormDesignations(request.POST)
            if form_designations.is_valid():
                meeting.designations = form_designations.save(commit=False)
            if meeting.type_meeting == 'w':
                form_weekendcontent = FormWeekendContent(request.POST)
                if form_weekendcontent.is_valid():
                    meeting.weekend_content = form_weekendcontent.save(commit=False)
            else:
                print(request.POST)
                form_midweekcontent = FormMidweekContent(request.POST)
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
                            item.person_treasure_id = request.POST.getlist('person_reading')[i]
                        else:
                            item.person_treasure_id = request.POST.getlist('person_treasure')[i]
                        meeting.midweek_content.treasures.append(item)
                    for i, title_apply in enumerate(request.POST.getlist('title_apply')):
                        item = ApplyYourselfContent(
                            title_apply=title_apply,
                            room_apply=request.POST.getlist('room_apply')[i],
                            duration_apply=request.POST.getlist('duration_apply')[i],
                            student_id=request.POST.getlist('student')[i],
                            assistant_id=request.POST.getlist('assistant')[i],
                        )

                        meeting.midweek_content.apply_yourself.append(item)
                    for i, title_living in enumerate(request.POST.getlist('title_living')):
                        item = LivingChristiansContent(
                            title_living=title_living,
                            duration_living=request.POST.getlist('duration_living')[i],
                            person_living_id=request.POST.getlist('person_living')[i],
                            reader_id=request.POST.getlist('reader')[i],
                        )

                        meeting.midweek_content.living_christians.append(item)
            meeting.save()
            messages.success(request, _("Meeting edited successfully"))
            return redirect('meetings')
    else:
        form = FormMeeting(instance=meeting)
        form_designations = FormDesignations(instance=meeting.designations)
        form_weekendcontent = FormWeekendContent(instance=meeting.weekend_content)
        form_midweekcontent = FormMidweekContent(instance=meeting.midweek_content)
        form_treasurescontent = FormTreasuresContent()
        form_applyyourselfcontent = FormApplyYourselfContent()
        form_livingchristianscontent = FormLivingChristiansContent()
        list_form_treasurescontent = []
        list_form_applyyourselfcontent = []
        list_form_livingchristianscontent = []
        if meeting.type_meeting == 'm':
            for f in meeting.midweek_content.treasures:
                initial = {}
                if f.reading:
                    initial['person_reading'] = f.person_treasure
                list_form_treasurescontent.append(FormTreasuresContent(instance=f, initial=initial))
            for f in meeting.midweek_content.apply_yourself:
                list_form_applyyourselfcontent.append(FormApplyYourselfContent(instance=f))
            for f in meeting.midweek_content.living_christians:
                list_form_livingchristianscontent.append(FormLivingChristiansContent(instance=f))
    return render(request, 'edit_meeting.html', {
        'request': request, 'form': form, 'app': 'meetings',
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
