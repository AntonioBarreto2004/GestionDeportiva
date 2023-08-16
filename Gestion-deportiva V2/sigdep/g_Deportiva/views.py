import pytz
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime
from .models import *

@api_view(['POST'])
def custom_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Verificar que los campos no estén vacíos
    if not email or not password:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'El email y la contraseña son requeridos',
            'data': None
        })

    # Obtener el usuario a través del email
    try:
        user = User.objects.get(people__email=email)
    except User.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Usuario no encontrado',
            'status': False
        })

    # Verificar la contraseña
    if not check_password(password, user.password):
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Contraseña incorrecta',
            'status': False
        })

    # Verificar si el usuario está autenticado
    if user.is_active:
        # Obtener el rol del usuario
        rol = user.rol

        if rol.name in ['Administrador', 'Instructor', 'Atleta']:
            # Generar los tokens de acceso y de actualización
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                'code': status.HTTP_200_OK,
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'message': f'Inicio de sesión exitoso con el Rol {rol.name}',
                'status': True
            })

    # Credenciales inválidas o usuario no autenticado o rol no permitido
    return Response({
        'code': status.HTTP_200_OK,
        'message': 'Credenciales inválidas, usuario no autenticado o rol no permitido',
        'status': False
    })

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def custom_logout(request):
#     refresh_token = request.data.get('refresh_token')

#     if not refresh_token:
#         return Response({
#             'code': status.HTTP_400_BAD_REQUEST,
#             'message': 'Se requiere el token de actualización para cerrar sesión',
#             'status': False
#         })

#     try:
#         refresh_token_obj = RefreshToken(refresh_token)
#         refresh_token_obj.blacklist()

#         # Asegurarse de que el token de actualización sea válido
#         if not refresh_token_obj.check_token(refresh_token):
#             return Response({
#                 'code': status.HTTP_400_BAD_REQUEST,
#                 'message': 'El token de actualización proporcionado no es válido',
#                 'status': False
#             })

#         # Eliminar el token de acceso del usuario actual
#         user = request.user
#         user.auth_token.delete()

#         return Response({
#             'code': status.HTTP_200_OK,
#             'message': 'Cierre de sesión exitoso',
#             'status': True
#         })
#     except Exception as e:
#         return Response({
#             'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
#             'message': 'Error al intentar cerrar sesión',
#             'status': False
#         })





#Actualizar fecha de cambios en los datos del usuario.
@receiver(pre_save, sender=People)
def profile_pre_save(sender, instance, **kwargs):
    if instance.pk:
        original_instance = People.objects.get(pk=instance.pk)
        if (
            original_instance.name != instance.name
            or original_instance.email != instance.email
            or original_instance.last_name != instance.last_name
            or original_instance.photo_user != instance.photo_user
            or original_instance.birthdate != instance.birthdate
            or original_instance.telephone_number != instance.telephone_number
            or original_instance.type_document != instance.type_document
        ):
            colombia_timezone = pytz.timezone('America/Bogota')
            # Obtener la fecha y hora actual en la zona horaria de Colombia
            current_time = datetime.now(colombia_timezone)
            # Asignar la fecha y hora actual en la zona horaria de Colombia al campo modified_at
            instance.modified_at = current_time

#Actualizar fecha de cambios
@receiver(pre_save, sender=Anthropometric)
def profile_pre_save(sender, instance, **kwargs):
    if instance.pk:
        original_instance = Anthropometric.objects.get(pk=instance.pk)
        if (
            original_instance.arm != instance.arm
            or original_instance.chest != instance.chest
            or original_instance.hip != instance.hip
            or original_instance.twin != instance.twin
            or original_instance.humerus != instance.humerus
            or original_instance.femur != instance.femur
            or original_instance.wrist != instance.wrist
            or original_instance.triceps != instance.triceps
            or original_instance.supraspinal != instance.supraspinal
            or original_instance.pectoral != instance.pectoral
            or original_instance.zise != instance.zise
            or original_instance.weight != instance.weight
            or original_instance.bmi != instance.bmi
        ):
            colombia_timezone = pytz.timezone('America/Bogota')
            # Obtener la fecha y hora actual en la zona horaria de Colombia
            current_time = datetime.now(colombia_timezone)
            # Asignar la fecha y hora actual en la zona horaria de Colombia al campo updated_date
            instance.updated_date = current_time






