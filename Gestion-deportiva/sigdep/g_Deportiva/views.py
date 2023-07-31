from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
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
            })

    # Credenciales inválidas o usuario no autenticado o rol no permitido
    return Response({
        'code': status.HTTP_200_OK,
        'message': 'Credenciales inválidas, usuario no autenticado o rol no permitido',
        'status': False
        }
    )
