from django.contrib import admin
from django.urls import path

from g_Deportiva.controllers import viewsUsers
from g_Deportiva.controllers import viewsRestPassword
from g_Deportiva.controllers import viewsUpdatePhoto
from g_Deportiva.controllers import viewsRole
from g_Deportiva.controllers import viewsDisability
from g_Deportiva.controllers import viewsAllergies
from g_Deportiva.controllers import viewsSports
from g_Deportiva.controllers import viewsTeam
from g_Deportiva.controllers import viewsAthlete
from g_Deportiva.controllers import viewsAthleteTeam
from g_Deportiva import views

urlpatterns = [
    path('list-users/', viewsUsers.list_users, name='list_users'),
    path('create-user/', viewsUsers.create_user, name='create_user'),
    path('update-user/<int:pk>/', viewsUsers.update_user, name='update_user'),
    path('delete-user/<people_id>/', viewsUsers.delete_user, name='delete_user'),
    path('update-photo/<people_id>/', viewsUpdatePhoto.update_profile_photo, name='Update Photo'),

    path('list-roles/', viewsRole.list_roles, name='list_roles'),
    path('create-role/', viewsRole.create_role, name='create_role'),
    path('update-role/<int:pk>/', viewsRole.update_role, name='update_role'),
    path('delete-role/<int:pk>/', viewsRole.delete_role, name='delete_role'),

    path('list-disabilities/', viewsDisability.list_disability, name='list_disability'),
    path('disabilities-create/', viewsDisability.create_disability, name='create_disability'),
    path('disabilities-update/<int:disability_id>/', viewsDisability.update_disability, name='update_disability'),
    path('disabilities-delete/<int:disability_id>/', viewsDisability.delete_disability, name='delete_disability'),

    path('list-allergies/', viewsAllergies.list_Allergies, name='list_Allergies'),
    path('allergies-create/', viewsAllergies.create_Allergies, name='create_Allergies'),
    path('allergies-update/<int:id>/', viewsAllergies.update_Allergies, name='update_Allergies'),
    path('allergies-delete/<int:id>/', viewsAllergies.delete_Allergies, name='delete_Allergies'),

    path('sports/', viewsSports.list_sports, name='list_sports'),
    path('sports-create/', viewsSports.create_sports, name='create_sports'),
    path('sports/<int:pk>/', viewsSports.sports_detail, name='sports_detail'),

    path('list-team/', viewsTeam.list_team, name='List Team'),
    path('create-team/', viewsTeam.create_team, name='Create Team'),
    path('update-team/<int:pk>/', viewsTeam.update_team, name='Update Team'),
    path('delete-team/<int:pk>/', viewsTeam.delete_team, name='Delete Team'),

    path('list-athlete/', viewsAthlete.list_athlete, name='list_athlete'),
    path('create-athlete/', viewsAthlete.create_athlete, name='create_athlete'),
    path('update-athlete/<int:pk>/', viewsAthlete.update_athlete, name='update_athlete'),
    path('delete-athlete/<int:pk>/', viewsAthlete.delete_athlete, name='delete_athlete'),

    path('list-athlete-team/', viewsAthleteTeam.list_athlete_team, name='list_athlete_team'),
    path('create-athlete-team/', viewsAthleteTeam.create_athlete_team, name='create_athlete_team'),
    path('update-athlete-team/<int:pk>/', viewsAthleteTeam.update_athlete_team, name='update_athlete_team'),
    path('delete-athlete-team/<int:pk>/', viewsAthleteTeam.delete_athlete_team, name='delete_athlete_team'),

    path('login/', views.custom_login, name='Login'),
    path('reset-password/', viewsRestPassword.reset_password, name='reset_Password'),
    path('reset-confirm/<str:uidb64>/<str:token>/', viewsRestPassword.reset_password_confirm, name='reset_password_confirm'),
]
