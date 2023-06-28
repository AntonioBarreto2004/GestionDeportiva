from django.urls import path
from seguimientoD import views


urlpatterns = [
    path('list-positions/', views.list_positions, name='List Positions'),
    path('create-positions/', views.create_positions, name='Create Position'),
    path('update-positions/<int:pk>/', views.update_positions, name='Update Position'),
    path('dalete-positions/<int:pk>/', views.delete_positions, name='Delete Position'),

    path('list-category/', views.list_category, name='List category'),
    path('create-category/', views.create_category, name='Create Categry'),
    path('update-category/<int:pk>/', views.update_category, name='Update Categry'),
    path('dalete-category/<int:pk>/', views.delete_category, name='Delete Categry'),

    path('list-team/', views.list_team, name='List Team'),
    path('create-team/', views.create_team, name='Create Team'),
    path('update-team/<int:pk>/', views.update_team, name='Update Team'),
    path('dalete-team/<int:pk>/', views.delete_team, name='Delete Team'),

    path('list-athlete/', views.list_athlete, name='List Athlete'),
    path('create-athlete/', views.create_athlete, name='Create Athlete'),
    path('update-athlete/<int:pk>/', views.update_athlete, name='Update Athlete'),
    path('dalete-athlete/<int:pk>/', views.delete_athlete, name='Delete Athlete'),
    
    path('list-anthrop/', views.list_anthro, name='List Anthropometric'),
    path('create-anthrop/', views.list_anthro, name='Create Anthropometric'),
    path('update-anthrop/<int:pk>/', views.list_anthro, name='Update Anthropometric'),
    path('dalete-anthrop/<int:pk>/', views.list_anthro, name='Delete Anthropometric'),
]