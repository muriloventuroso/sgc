from django.urls import path
import users.views

urlpatterns = [

    path('<user_id>/delete/', users.views.delete_user, {}, 'delete_user'),
    path('<user_id>/edit/', users.views.edit_user, {}, 'edit_user'),
    path('add/', users.views.add_user, {}, 'add_user'),
    path('password/', users.views.change_password, {}, 'change_password'),
    path('<user_id>/password/', users.views.set_password, {}, 'set_password'),
    path('resources/', users.views.get_resources, {}, 'user_resources'),
    path('', users.views.users, {}, 'users'),
]
