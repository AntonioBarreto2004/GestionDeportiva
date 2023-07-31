from django.contrib import admin
from django.urls import path
from g_Deportiva.controllers import viewsSports
from g_Deportiva.controllers import viewsUsers
from g_Deportiva.controllers import viewsTeam
urlpatterns = [
    path('list-users/', viewsUsers.list_users, name='list_users'),
    path('create-user/', viewsUsers.create_user, name='create_user'),
    
    path('sports/', viewsSports.list_sports, name='list_sports'),
    path('sports-create/', viewsSports.create_sports, name='create_sports'),
    path('sports/<int:pk>/', viewsSports.sports_detail, name='sports_detail'),

    path('list-team/', viewsTeam.list_team, name='List Team'),
    path('create-team/', viewsTeam.create_team, name='Create Team'),
    path('update-team/<int:pk>/', viewsTeam.update_team, name='Update Team'),
    path('delete-team/<int:pk>/', viewsTeam.delete_team, name='Delete Team'),
]

