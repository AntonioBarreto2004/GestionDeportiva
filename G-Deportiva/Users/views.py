import jwt
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.db.models.signals import pre_save
from django.dispatch import receiver
import pytz
from datetime import datetime
from .models import *
from .serializers import *

@api_view(['POST'])
def custom_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Realizar la autenticación del usuario
    user = authenticate(request, email=email, password=password)

    if user is not None and user.is_authenticated:
        # Obtener el ID del rol del usuario
        rol_id = user.cod_rol_id

        try:
            # Buscar el rol por ID
            rol = Rol.objects.get(id=rol_id)
        except Rol.DoesNotExist:
            return Response({
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Rol no encontrado',
                'status': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if rol.name_rol in ['Administrador', 'Instructor', 'Atleta']:
            # Generar los tokens de acceso y de actualización
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                'code': status.HTTP_200_OK,
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'message': f'Inicio de sesión exitoso con el Rol {rol.name_rol}',
                'status': True
            }, status=status.HTTP_200_OK)

    # Credenciales inválidas o usuario no autenticado o rol no permitido
    return Response({
        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'message': 'Credenciales inválidas, usuario no autenticado o rol no permitido',
        'status': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def system_access(request):
    try:
        # Verificar el token de acceso
        access_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise AuthenticationFailed('Token inválido o expirado')

    return Response({'message': 'Acceso permitido'})





#Actualizar fecha de cambios en los datos del usuario.
@receiver(pre_save, sender=User)
def profile_pre_save(sender, instance, **kwargs):
    if instance.pk:
        original_instance = User.objects.get(pk=instance.pk)
        if (
            original_instance.name != instance.name
            or original_instance.email != instance.email
            or original_instance.last_name != instance.last_name
            or original_instance.photo_profile != instance.photo_profile
            or original_instance.birthdate != instance.birthdate
            or original_instance.telephone_number != instance.telephone_number
        ):
            colombia_timezone = pytz.timezone('America/Bogota')
            # Obtener la fecha y hora actual en la zona horaria de Colombia
            current_time = datetime.now(colombia_timezone)
            # Asignar la fecha y hora actual en la zona horaria de Colombia al campo modified_at
            instance.modified_at = current_time



