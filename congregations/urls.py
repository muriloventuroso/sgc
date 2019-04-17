from django.urls import path
import congregations.views

urlpatterns = [

    path(
        'roles/<congregation_role_id>/delete/', congregations.views.delete_congregation_role,
        {}, 'delete_congregation_role'),
    path(
        'roles/<congregation_role_id>/edit/', congregations.views.edit_congregation_role,
        {}, 'edit_congregation_role'),
    path('roles/add/', congregations.views.add_congregation_role, {}, 'add_congregation_role'),
    path('roles/', congregations.views.congregation_roles, {}, 'congregation_roles'),

    path('groups/<group_id>/delete/', congregations.views.delete_group, {}, 'delete_group'),
    path('groups/<group_id>/edit/', congregations.views.edit_group, {}, 'edit_group'),
    path('groups/add/', congregations.views.add_group, {}, 'add_group'),
    path('groups/', congregations.views.groups, {}, 'groups'),

    path('publishers/<publisher_id>/delete/', congregations.views.delete_publisher, {}, 'delete_publisher'),
    path('publishers/<publisher_id>/edit/', congregations.views.edit_publisher, {}, 'edit_publisher'),
    path('publishers/add/', congregations.views.add_publisher, {}, 'add_publisher'),
    path('publishers/', congregations.views.publishers, {}, 'publishers'),

    path('<congregation_id>/delete/', congregations.views.delete_congregation, {}, 'delete_congregation'),
    path('<congregation_id>/edit/', congregations.views.edit_congregation, {}, 'edit_congregation'),
    path('add/', congregations.views.add_congregation, {}, 'add_congregation'),
    path('', congregations.views.congregations, {}, 'congregations'),
]
