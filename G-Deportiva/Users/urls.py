from django.urls import path
from Users.Controllers import viewsDocumentType
from Users.Controllers import viewsRole
from Users.Controllers import viewsU
from Users.Controllers import viewsGender
from Users.Controllers import viewsExportPdf
from Users.Controllers import viewsExportExcel
from Users.Controllers import viewsRestPassword
from Users.Controllers import viewsUpdatePhoto
from Users import views


urlpatterns = [

    path('list-document-types/', viewsDocumentType.list_document_types, name='list_document_types'),
    path('create-document-type/', viewsDocumentType.create_document_type, name='create_document_type'),
    path('update-document-type/<int:pk>/', viewsDocumentType.update_document_type, name='update_document_type'),
    path('delete-document-type/<int:pk>/', viewsDocumentType.delete_document_type, name='delete_document_type'),

    path('list-roles/', viewsRole.list_roles, name='list_roles'),
    path('create-role/', viewsRole.create_role, name='create_role'),
    path('update-role/<int:pk>/', viewsRole.update_role, name='update_role'),
    path('delete-role/<int:pk>/', viewsRole.delete_role, name='delete_role'),
    path('update-photo/<user_id>/', viewsUpdatePhoto.update_profile_photo, name='Update Photo'),

    
    path('list-users/', viewsU.list_users, name='list_users'),
    path('create-user/', viewsU.create_user, name='create_user'),
    path('update-user/<int:pk>/', viewsU.update_user, name='update_user'),
    path('delete-user/<int:pk>/', viewsU.delete_user, name='delete_user'),


    path('list-gender/', viewsGender.list_genders, name='list_users'),
    path('create-gender/', viewsGender.create_gender, name='create_Gender'),
    path('update-gender/<int:pk>/', viewsGender.update_gender, name='update_Gender'),
    path('delete-gender/<int:pk>/', viewsGender.delete_gender, name='delete_Gender'),

    path('login/', views.custom_login, name='Login'),
    path('token-acceso/', views.system_access, name='Access Token'),

    path('export-pdf/', viewsExportPdf.export_users_to_pdf, name='export_users'),
    path('export-excel/', viewsExportExcel.export_users_to_excel, name='export_users'),

    path('reset-password/', viewsRestPassword.reset_password, name='reset_Password'),
    path('reset-confirm/<str:uidb64>/<str:token>/', viewsRestPassword.reset_password_confirm, name='password_reset_confirm'),

    
]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

