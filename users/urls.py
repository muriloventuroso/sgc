from django.urls import path
import users.views

urlpatterns = [

    path('<user_id>/delete/', users.views.delete_user, {}, 'delete_user'),
    path('<user_id>/edit/', users.views.edit_user, {}, 'edit_user'),
    path('add/', users.views.add_user, {}, 'add_user'),
    path('', users.views.users, {}, 'users'),
]
