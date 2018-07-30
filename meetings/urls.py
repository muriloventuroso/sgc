from django.urls import path
import meetings.views

urlpatterns = [

    path('', meetings.views.meetings, {}, 'meetings'),
]
