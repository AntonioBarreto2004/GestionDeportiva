from django.urls import path

from seguimientoD.Controllers import viewsAnthropometric
from seguimientoD.Controllers import viewsAnthropHistory
from seguimientoD.Controllers import viewsPositions
from seguimientoD.Controllers import viewsCategory
from seguimientoD.Controllers import viewsTeam
from seguimientoD.Controllers import viewsAthlete
from seguimientoD.Controllers import viewsCompareChanges


urlpatterns = [
    path('list-positions/', viewsPositions.list_positions, name='List Positions'),
    path('create-positions/', viewsPositions.create_positions, name='Create Position'),
    path('update-positions/<int:pk>/', viewsPositions.update_positions, name='Update Position'),
    path('dalete-positions/<int:pk>/', viewsPositions.delete_positions, name='Delete Position'),

    path('list-category/', viewsCategory.list_category, name='List category'),
    path('create-category/', viewsCategory.create_category, name='Create Categry'),
    path('update-category/<int:pk>/', viewsCategory.update_category, name='Update Categry'),
    path('dalete-category/<int:pk>/', viewsCategory.delete_category, name='Delete Categry'),

    path('list-team/', viewsTeam.list_team, name='List Team'),
    path('create-team/', viewsTeam.create_team, name='Create Team'),
    path('update-team/<int:pk>/', viewsTeam.update_team, name='Update Team'),
    path('delete-team/<int:pk>/', viewsTeam.delete_team, name='Delete Team'),

    path('list-athlete/', viewsAthlete.list_athlete, name='List Athlete'),
    path('create-athlete/', viewsAthlete.create_athlete, name='Create Athlete'),
    path('update-athlete/<int:pk>/', viewsAthlete.update_athlete, name='Update Athlete'),
    path('dalete-athlete/<int:pk>/', viewsAthlete.delete_athlete, name='Delete Athlete'),
    
    path('list-anthrop/', viewsAnthropometric.list_anthro, name='List Anthropometric'),
    path('create-anthrop/', viewsAnthropometric.create_anthro, name='Create Anthropometric'),
    path('update-anthrop/<int:pk>/', viewsAnthropometric.update_anthro, name='Update Anthropometric'),
    path('dalete-anthrop/<int:pk>/', viewsAnthropometric.delete_anthro, name='Delete Anthropometric'),

    path('list-anthrop-history/', viewsAnthropHistory.list_anthro, name='List Anthropometric'),
    path('create-anthrop-history/', viewsAnthropHistory.create_anthro, name='Create Anthropometric'),
    path('update-anthrop-history/<int:pk>/', viewsAnthropHistory.update_anthro, name='Update Anthropometric'),
    path('dalete-anthrop-history/<int:pk>/', viewsAnthropHistory.delete_anthro, name='Delete Anthropometric'),

    path('compare-changes/', viewsCompareChanges.compare_changes, name='Compare Changes'),
]