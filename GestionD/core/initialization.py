from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from .models import Rol

class CreateGroupsCommand(BaseCommand):
    def handle(self, *args, **options):
        # Crear grupos
        grupo_admin, _ = Group.objects.get_or_create(name='Admin')
        grupo_instructor, _ = Group.objects.get_or_create(name='Instructor')
        grupo_usuarios, _ = Group.objects.get_or_create(name='Cliente_Persona')

        # Obtener todos los permisos disponibles
        todos_los_permisos = Permission.objects.all()

        # Asignar todos los permisos al grupo Admin
        grupo_admin.permissions.set(todos_los_permisos)

        # Obtener o crear permisos
        permisos_instructor = Permission.objects.filter(codename__in=['view_user', 'view_rol', 'view_profile', 'change_profile',
                                                                      'add_category', 'change_category', 'delete_category', 'view_category',
                                                                      'add_positions', 'change_positions', 'delete_positions', 'view_positions',
                                                                      'add_athlete', 'change_athlete', 'delete_athlete', 'view_athlete',
                                                                      'add_team', 'change_team', 'delete_team', 'view_team', 
                                                                      'view_anthropometric', 'add_anthropometric', 'change_anthropometric', 'view_anthropometric'])
        
        permisos_usuarios = Permission.objects.filter(codename__in=['view_user', 'view_rol', 'view_profile', 'change_profile',
                                                                    'view_category',
                                                                    'view_positions',
                                                                    'view_athlete',
                                                                    'view_team', 
                                                                    'view_anthropometric', 'add_anthropometric', 'change_anthropometric'])

        # Asignar permisos a los grupos
        grupo_instructor.permissions.set(permisos_instructor)
        grupo_usuarios.permissions.set(permisos_usuarios)

        # Asignar grupos a los roles correspondientes
        rol_admin = Rol.objects.get(name_rol='Admin')
        rol_admin.group = grupo_admin
        rol_admin.save()

        rol_instructor = Rol.objects.get(name_rol='Instructor')
        rol_instructor.group = grupo_instructor
        rol_instructor.save()

        rol_usuarios = Rol.objects.get(name_rol='Cliente_Persona')
        rol_usuarios.group = grupo_usuarios
        rol_usuarios.save()
