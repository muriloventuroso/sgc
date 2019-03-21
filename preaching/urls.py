from django.urls import path
import preaching.views

urlpatterns = [

    path(
        'preaching/pioneers/<pioneer_id>/delete/', preaching.views.delete_pioneer,
        {}, 'delete_pioneer'),
    path('preaching/pioneers/<pioneer_id>/edit/', preaching.views.edit_pioneer, {}, 'edit_pioneer'),
    path('preaching/pioneers/add/', preaching.views.add_pioneer, {}, 'add_pioneer'),
    path('preaching/pioneers/', preaching.views.pioneers, {}, 'pioneers'),
]
