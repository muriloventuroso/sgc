from django.urls import path
import meetings.views

urlpatterns = [
    path('<meeting_id>/delete/', meetings.views.delete_meeting, {}, 'delete_meeting'),
    path('<meeting_id>/edit/', meetings.views.edit_meeting, {}, 'edit_meeting'),
    path('add/', meetings.views.add_meeting, {}, 'add_meeting'),
    path('', meetings.views.meetings, {}, 'meetings'),
]
