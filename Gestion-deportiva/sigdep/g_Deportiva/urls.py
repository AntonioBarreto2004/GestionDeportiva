from django.contrib import admin
from django.urls import path

from g_Deportiva.controllers import viewsUsers
urlpatterns = [
    path('list-users/', viewsUsers.list_users, name='list_users'),
    path('create-user/', viewsUsers.create_user, name='create_user'),
]
