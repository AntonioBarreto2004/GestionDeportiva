from django.urls import path
from .views import TournamentListCreateView, TournamentRetrieveUpdateDestroyView

urlpatterns = [
    path('tournaments/', TournamentListCreateView.as_view(), name='tournament-list-create'),
    path('tournaments/<int:pk>/', TournamentRetrieveUpdateDestroyView.as_view(), name='tournament-retrieve-update-destroy'),
]