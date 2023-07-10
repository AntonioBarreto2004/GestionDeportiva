from django.urls import path, include
from core.Controllers import viewsDocumentType
from core.Controllers import viewsRole
from core.Controllers import viewsU
from core.Controllers import viewsProfile
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('list-document-types/', viewsDocumentType.list_document_types, name='list_document_types'),
    path('create-document-type/', viewsDocumentType.create_document_type, name='create_document_type'),
    path('update-document-type/<int:pk>/', viewsDocumentType.update_document_type, name='update_document_type'),
    path('delete-document-type/<int:pk>/', viewsDocumentType.delete_document_type, name='delete_document_type'),

    path('list-roles/', viewsRole.list_roles, name='list_roles'),
    path('create-role/', viewsRole.create_role, name='create_role'),
    path('update-role/<int:pk>/', viewsRole.update_role, name='update_role'),
    path('delete-role/<int:pk>/', viewsRole.delete_role, name='delete_role'),

    path('list-profiles/', viewsProfile.list_profiles, name='list_profiles'),
    path('create-profile/', viewsProfile.create_profile, name='create_profile'),
    path('update-profile/<int:pk>/', viewsProfile.update_profile, name='update_profile'),
    path('delete-profile/<int:pk>/', viewsProfile.delete_profile, name='delete_profile'),
    
    path('list-users/', viewsU.list_users, name='list_users'),
    path('create-user/', viewsU.create_user, name='create_user'),
    path('update-user/<int:pk>/', viewsU.update_user, name='update_user'),
    path('delete-user/<int:pk>/', viewsU.delete_user, name='delete_user'),

    path('login/', views.login_api, name='Login')
]

