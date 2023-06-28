from django.urls import path, include
from rest_framework import routers
from core import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('list-document-types/', views.list_document_types, name='list_document_types'),
    path('create-document-type/', views.create_document_type, name='create_document_type'),
    path('update-document-type/<int:pk>/', views.update_document_type, name='update_document_type'),
    path('delete-document-type/<int:pk>/', views.delete_document_type, name='delete_document_type'),

    path('list-roles/', views.list_roles, name='list_roles'),
    path('create-role/', views.create_role, name='create_role'),
    path('update-role/<int:pk>/', views.update_role, name='update_role'),
    path('delete-role/<int:pk>/', views.delete_role, name='delete_role'),

    path('list-profiles/', views.list_profiles, name='list_profiles'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('update-profile/<int:pk>/', views.update_profile, name='update_profile'),
    path('delete-profile/<int:pk>/', views.delete_profile, name='delete_profile'),
    
    path('list-users/', views.list_users, name='list_users'),
    path('create-user/', views.create_user, name='create_user'),
    path('update-user/<int:pk>/', views.update_user, name='update_user'),
    path('delete-user/<int:pk>/', views.delete_user, name='delete_user'),
]

