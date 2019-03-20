from django.urls import path
import meetings.views

urlpatterns = [
    path(
        'audiences/<meeting_audience_id>/delete/', meetings.views.delete_meeting_audience,
        {}, 'delete_meeting_audience'),
    path('audiences/<meeting_audience_id>/edit/', meetings.views.edit_meeting_audience, {}, 'edit_meeting_audience'),
    path('audiences/add/', meetings.views.add_meeting_audience, {}, 'add_meeting_audience'),
    path('audiences/', meetings.views.meeting_audiences, {}, 'meeting_audiences'),

    path('<meeting_id>/delete/', meetings.views.delete_meeting, {}, 'delete_meeting'),
    path('<meeting_id>/edit/', meetings.views.edit_meeting, {}, 'edit_meeting'),
    path('add/', meetings.views.add_meeting, {}, 'add_meeting'),
    path('pdf/', meetings.views.generate_pdf, {}, 'generate_pdf'),
    path('suggest/publisher/', meetings.views.suggest_publisher, {}, 'suggest_publisher'),
    path('suggest/meeting/', meetings.views.suggest_meeting, {}, 'suggest_meeting'),
    path('', meetings.views.meetings, {}, 'meetings'),
]
