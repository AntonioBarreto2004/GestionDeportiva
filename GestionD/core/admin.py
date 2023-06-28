from django.contrib import admin
from .models import *

admin.site.register(User)

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
  list_display = ['name']

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
  list_display = ['name_rol']
  search_fields = ['name_rol']
  list_per_page = 5

# Register your models here.
@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
  list_display = ['user', 'type_document', 'num_document', 'telephone_number', 'birthdate', 'gender','Imagen_del_usuario', 'allergies', 'disability', 'date_create', "cod_rol", "state", "file", "file_v", "file_f"]
  list_editable = ['telephone_number', "state"]
  search_fields = ['num_document']
  list_filter = ['date_create']
  list_per_page = 5




  