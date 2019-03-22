from django.urls import path
import preaching.views

urlpatterns = [

    path(
        'preaching/pioneers/<pioneer_id>/delete/', preaching.views.delete_pioneer,
        {}, 'delete_pioneer'),
    path('preaching/pioneers/<pioneer_id>/edit/', preaching.views.edit_pioneer, {}, 'edit_pioneer'),
    path('preaching/pioneers/add/', preaching.views.add_pioneer, {}, 'add_pioneer'),
    path('preaching/pioneers/', preaching.views.pioneers, {}, 'pioneers'),

    path(
        'preaching/reports/<field_service_report_id>/delete/', preaching.views.delete_field_service_report,
        {}, 'delete_field_service_report'),
    path(
        'preaching/reports/<field_service_report_id>/edit/', preaching.views.edit_field_service_report,
        {}, 'edit_field_service_report'),
    path('preaching/reports/add/', preaching.views.add_field_service_report, {}, 'add_field_service_report'),
    path('preaching/reports/', preaching.views.field_service_reports, {}, 'field_service_reports'),
]
