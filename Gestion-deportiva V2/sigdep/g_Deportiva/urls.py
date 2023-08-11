from django.urls import path
from g_Deportiva.controllers import viewsPeople
from g_Deportiva.controllers import viewsRestPassword
from g_Deportiva.controllers import viewsUpdatePhoto
from g_Deportiva.controllers import viewsRole
from g_Deportiva.controllers import viewsDisability
from g_Deportiva.controllers import viewsAllergies
from g_Deportiva.controllers import viewsSports
from g_Deportiva.controllers import viewsTeam
from g_Deportiva.controllers import viewsInstructor
from g_Deportiva.controllers import viewsAnthropometric
from g_Deportiva.controllers import viewsCompareChanges
from g_Deportiva.controllers import viewsCategory
from g_Deportiva.controllers import viewsAthlete
from g_Deportiva.controllers import viewsExportPdf
from g_Deportiva.controllers import viewsSpecial_conditions
from g_Deportiva import views

urlpatterns = [
    path('list-peoples/', viewsPeople.list_users, name='list_users'),
    path('create-people/', viewsPeople.create_user, name='create_user'),
    path('update-people/<int:pk>/', viewsPeople.update_user, name='update_user'),
    path('delete-people/<int:pk>/', viewsPeople.delete_user, name='delete_user'),
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
    path('allergies-update/<int:pk>/', viewsAllergies.update_Allergies, name='update_Allergies'),
    path('allergies-delete/<int:pk>/', viewsAllergies.delete_Allergies, name='delete_Allergies'),

    path('sports/', viewsSports.list_sports, name='list_sports'),
    path('sports-create/', viewsSports.create_sports, name='create_sports'),
    path('sports-update/<int:pk>/', viewsSports.update_sport, name='sports_detail'),
    path('sports-delete/<int:pk>/', viewsSports.delete_sport, name='sports_detail'),
    path('sports-state/', viewsSports.state_sport, name='desacive_sports'),

    path('list-team/', viewsTeam.list_team, name='List Team'),
    path('create-team/', viewsTeam.create_team, name='Create Team'),
    path('update-team/<int:pk>/', viewsTeam.update_team, name='Update Team'),
    path('delete-team/<int:pk>/', viewsTeam.delete_team, name='Delete Team'),

    path('list-instructors/', viewsInstructor.list_instructors, name='List instructors'),
    path('create-instructor/', viewsInstructor.create_instructor, name='create instructors'),
    path('update-instructor/<int:pk>/', viewsInstructor.update_instructor, name='Update instructors'),
    path('delete-instructor/<int:pk>/', viewsInstructor.delete_instructor, name='Delete instructors'),

    path('list-anthrop/', viewsAnthropometric.list_anthro, name='List Anthropometric'),
    path('create-anthrop/', viewsAnthropometric.create_anthro, name='Create Anthropometric'),
    path('update-anthrop/<int:pk>/', viewsAnthropometric.update_anthro, name='Update Anthropometric'),
    path('dalete-anthrop/<int:pk>/', viewsAnthropometric.delete_anthro, name='Delete Anthropometric'),

    path('compare-changes/', viewsCompareChanges.compare_changes, name='Compare Changes'),

    path('list-category/', viewsCategory.list_category, name='list Category'),
    path('create-category/', viewsCategory.create_category, name='create Category'),
    path('update-category/<int:pk>/', viewsCategory.update_category, name='update Category'),
    path('delete-category/<int:pk>/', viewsCategory.delete_category, name='delete Category'),

    path('list-athlete/', viewsAthlete.list_athlete, name='List Athlete'),
    path('create-athlete/', viewsAthlete.create_athlete, name='Create Athlete'),
    path('update-athlete/<int:pk>/', viewsAthlete.update_athlete, name='Update Athlete'),
    path('delete-athlete/<int:pk>/', viewsAthlete.delete_athlete, name='Delete Athlete'),
    path('athlete-state/', viewsAthlete.state_atlete, name='status atleta'),

    path('export-pdf/', viewsExportPdf.export_users_to_pdf, name='export_users'),

    path('special-conditions/', viewsSpecial_conditions.list_special_conditions, name='list_special_conditions'),
    path('special-conditions-create/', viewsSpecial_conditions.create_special_condition, name='create_special_condition'),
    path('special-conditions-update/<int:condition_id>/', viewsSpecial_conditions.update_special_condition, name='update_special_condition'),
    path('special-conditions-delete/<int:pk>/', viewsSpecial_conditions.delete_special_condition, name='delete_special_condition'),

    path('login/', views.custom_login, name='Login'),
    path('reset-password/', viewsRestPassword.reset_password, name='reset_Password'),
    path('reset-confirm/<str:uidb64>/<str:token>/', viewsRestPassword.reset_password_confirm, name='reset_password_confirm'),
    
]
